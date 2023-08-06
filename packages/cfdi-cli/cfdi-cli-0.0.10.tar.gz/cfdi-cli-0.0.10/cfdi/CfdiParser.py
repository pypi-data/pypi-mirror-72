import xmltodict
import json
import base64
import tempfile
from suds.client import Client, WebFault
from enum import Enum


class SATStates(Enum):
    RETRY = "Retry"
    NOT_FOUND = "No Encontrado"
    OK = "Vigente"

    @staticmethod
    def check(state):
        return state in [a.value for a in SATStates]


# noinspection SpellCheckingInspection
class CfdiParser(object):
    VERSIONS = ["3.3"]
    SAT_STATES = ["No Encontrado"]

    version = None
    serie = None
    folio = None
    fecha = None
    moneda = None
    subtotal = None
    total = None
    descuento = None
    tipo_cambio = None
    tipo_comprobante = None
    forma_pago = None
    metodo_pago = None
    condiciones_pago = None
    lugar_exp = None
    confirmacion = None
    no_cert = None
    sello = None
    certificado = None
    emisor_rfc = None
    receptor_rfc = None
    uuid = None
    state = SATStates.RETRY

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<cfdi:Comprobante Version={} Fecha={} state={}>".format(
            self.version, self.fecha, SATStates(self.state))

    def check_cfdi_service(self):
        if not (self.uuid and self.emisor_rfc and self.receptor_rfc and self.total):
            return SATStates.NOT_FOUND.value

        request = '?re=' + str(self.emisor_rfc) + '&rr=' + str(self.receptor_rfc) + '&tt=' + str(
            self.total) + '&id=' + str(self.uuid)
        client = Client('https://consultaqr.facturaelectronica.sat.gob.mx/ConsultaCFDIService.svc?wsdl')
        client.set_options(timeout=60)
        result = client.service.Consulta(request)
        estado = result.Estado
        if SATStates.check(estado):
            return estado
        else:
            print("Error parsing state: {}".format(estado))
            return SATStates.NOT_FOUND.value

    def load_xml_from_base64(self, b64):
        data = base64.b64decode(b64).decode()
        file = tempfile.NamedTemporaryFile()
        with open(file.name, "wb") as f:
            f.write(data)
        return self.load_xml(file.name)

    def load_xml(self, xml_file: str):
        with open(xml_file, "rb") as f:
            xml = f.read().decode()
            xml_odict = xmltodict.parse(xml, attr_prefix="")
            xml_dict = json.loads(json.dumps(xml_odict))
            comprobante = xml_dict.get("cfdi:Comprobante", {})
            assert isinstance(comprobante, dict)

            comprobante.pop("xmlns:xsi", None)
            comprobante.pop("xmlns:cfdi", None)
            comprobante.pop("xsi:schemaLocation", None)
            comprobante.pop("xmlns:nomina12", None)
            emisor = comprobante.pop("cfdi:Emisor", None)
            receptor = comprobante.pop("cfdi:Receptor", None)
            comprobante.pop("cfdi:Conceptos", None)
            complemento = comprobante.pop("cfdi:Complemento", None)
            # Todo(@jorgejuarezcasai) validate related cfdis
            comprobante.pop("cfdi:CfdiRelacionados", None)
            # Todo(@jorgejuarezcasai) validate taxes
            comprobante.pop("cfdi:Impuestos", None)

            # Version are required
            self.version = comprobante.pop("Version", None)
            assert self.version in self.VERSIONS, "Wrong CFDI Version"

            self.serie = comprobante.pop("Serie", None)
            self.folio = comprobante.pop("Folio", None)
            self.fecha = comprobante.pop("Fecha", None)
            self.moneda = comprobante.pop("Moneda", "MXN")
            self.subtotal = comprobante.pop("SubTotal", None)
            self.descuento = comprobante.pop("Descuento", None)
            self.total = comprobante.pop("Total", None)
            self.tipo_cambio = comprobante.pop("TipoCambio", 1.0)
            self.tipo_comprobante = comprobante.pop("TipoDeComprobante", None)
            self.forma_pago = comprobante.pop("FormaPago", None)
            self.metodo_pago = comprobante.pop("MetodoPago", None)
            self.condiciones_pago = comprobante.pop("CondicionesDePago", None)
            self.lugar_exp = comprobante.pop("LugarExpedicion", None)
            self.confirmacion = comprobante.pop("Confirmacion", None)
            self.no_cert = comprobante.pop("NoCertificado", None)
            self.certificado = comprobante.pop("Certificado", None)
            self.sello = comprobante.pop("Sello", None)
            self.emisor_rfc = emisor.pop("Rfc", None)
            self.receptor_rfc = receptor.pop("Rfc", None)

            assert len(comprobante.keys()) == 0, "XML has extra elements %s" % (comprobante,)
            assert self.emisor_rfc, "RFC de Emisor no encontrado"
            assert self.receptor_rfc, "RFC de Receptor no encontrado"

            if complemento:
                tfd = complemento.pop("tfd:TimbreFiscalDigital", None)
                self.uuid = tfd.pop("UUID", None)

            self.state = self.check_cfdi_service()
            success = SATStates.check(self.state)
            return success
