from django.core.exceptions import ValidationError
from django.test import TestCase

from openwisp_users.tests.utils import TestOrganizationMixin

from ...pki.models import Ca, Cert
from ..models import Config, Device, Template, Vpn
from . import CreateConfigTemplateMixin, TestVpnX509Mixin


class TestTemplate(
    CreateConfigTemplateMixin, TestVpnX509Mixin, TestOrganizationMixin, TestCase
):
    ca_model = Ca
    cert_model = Cert
    config_model = Config
    device_model = Device
    template_model = Template
    vpn_model = Vpn

    def test_template_with_org(self):
        org = self._create_org()
        template = self._create_template(organization=org)
        self.assertEqual(template.organization_id, org.pk)

    def test_template_without_org(self):
        template = self._create_template()
        self.assertIsNone(template.organization)

    def test_template_with_shared_vpn(self):
        vpn = self._create_vpn()  # shared VPN
        org = self._create_org()
        template = self._create_template(organization=org, type='vpn', vpn=vpn)
        self.assertIsNone(vpn.organization)
        self.assertEqual(template.vpn_id, vpn.pk)

    def test_template_and_vpn_different_organization(self):
        org1 = self._create_org()
        vpn = self._create_vpn(organization=org1)
        org2 = self._create_org(name='test org2', slug='test-org2')
        try:
            self._create_template(organization=org2, type='vpn', vpn=vpn)
        except ValidationError as e:
            self.assertIn('organization', e.message_dict)
            self.assertIn('related VPN server match', e.message_dict['organization'][0])
        else:
            self.fail('ValidationError not raised')

    def test_org_default_template(self):
        org1 = self._create_org(name='org1')
        org2 = self._create_org(name='org2')
        self._create_template(organization=org1, name='t1', default=True)
        self._create_template(organization=org2, name='t2', default=True)
        d1 = self._create_device(organization=org1, name='d1')
        c1 = self._create_config(device=d1)
        self.assertEqual(c1.templates.count(), 1)
        self.assertEqual(c1.templates.filter(name='t1').count(), 1)
        d2 = self._create_device(
            organization=org2,
            name='d2',
            mac_address='00:00:00:11:22:33',
            key='1234567890',
        )
        c2 = self._create_config(device=d2)
        self.assertEqual(c2.templates.count(), 1)
        self.assertEqual(c2.templates.filter(name='t2').count(), 1)

    def test_org_default_shared_template(self):
        org1 = self._create_org(name='org1')
        self._create_template(organization=org1, name='t1', default=True)
        self._create_template(organization=None, name='t2', default=True)
        c1 = self._create_config(organization=org1)
        self.assertEqual(c1.templates.count(), 2)
        self.assertEqual(c1.templates.filter(name='t1').count(), 1)
        self.assertEqual(c1.templates.filter(name='t2').count(), 1)

    def test_auto_client_template(self):
        org = self._create_org()
        vpn = self._create_vpn(organization=org)
        t = self._create_template(
            name='autoclient',
            organization=org,
            type='vpn',
            auto_cert=True,
            vpn=vpn,
            config={},
        )
        control = t.vpn.auto_client()
        self.assertDictEqual(t.config, control)

    def test_auto_client_template_default(self):
        org = self._create_org()
        vpn = self._create_vpn(organization=org)
        self._create_template(
            name='autoclient',
            organization=org,
            default=True,
            type='vpn',
            auto_cert=True,
            vpn=vpn,
            config={},
        )
        self._create_config(organization=org)

    def test_auto_generated_certificate_for_organization(self):
        organization = self._create_org()
        vpn = self._create_vpn()
        template = self._create_template(type='vpn', auto_cert=True, vpn=vpn)
        corresponding_device = self._create_device(organization=organization,)
        config = self._create_config(device=corresponding_device,)
        config.templates.add(template)
        vpn_clients = config.vpnclient_set.all()
        for vpn_client in vpn_clients:
            self.assertIsNotNone(vpn_client.cert.organization)
            self.assertEqual(vpn_client.cert.organization, config.device.organization)

    def test_template_name_and_organization_unique(self):
        org = self._create_org()
        self._create_template(name='template', organization=org, default=True)
        kwargs = {
            'name': 'template',  # the name attribute is same as in the template created
            'organization': org,
            'default': True,
        }
        # _create_template should raise an exception as
        # two templates with the same organization can't have the same name
        with self.assertRaises(ValidationError):
            self._create_template(**kwargs)
