# coding: UTF-8
""" This file contain classes corresponding to materialsdb*.xsd elements.
This file is automatically generated. Do not modify it directly.
If there is an issue or an enhancement to make then do it in dataclasses_generator.py

© All rights reserved.
ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, Laboratory CNPA, 2019-2020

See the LICENSE.md file for more details.

Author : Cyril Waechter
"""
from dataclasses import dataclass
from typing import Tuple, Optional, List


class TLCADB(str):
    xs_type: str = "simpleType"
    xml_enum: Tuple[str, ...] = ('dbKBOB', 'dbOkobauDat', 'dbLux')
    xml_name: str = "TLCADB"


class TFireComb(str):
    xs_type: str = "simpleType"
    xml_enum: Tuple[str, ...] = ('3', '4', '5', '5_200C', '6q', '6')
    xml_name: str = "TFireComb"


class TFireSmoke(str):
    xs_type: str = "simpleType"
    xml_enum: Tuple[str, ...] = ('1', '2', '3')
    xml_name: str = "TFireSmoke"


class TFireResis(str):
    xs_type: str = "simpleType"
    xml_enum: Tuple[str, ...] = ('A1', 'A2', 'B', 'C', 'D', 'E', 'F')
    xml_name: str = "TFireResis"


class TFireReact(str):
    xs_type: str = "simpleType"
    xml_enum: Tuple[str, ...] = ('RF1', 'RF2', 'RF2cr', 'RF3', 'RF3cr', 'RF4cr')
    xml_name: str = "TFireReact"


class TFireDin4102(str):
    xs_type: str = "simpleType"
    xml_enum: Tuple[str, ...] = ('A1', 'A2', 'B1', 'B2', 'B3')
    xml_name: str = "TFireDin4102"


class T2Lowercase(str):
    xs_type: str = "simpleType"
    xml_pattern:str = "[a-z][a-z]"
    xml_name: str = "T2Lowercase"


class Groupkind(str):
    xs_type: str = "simpleType"
    xml_enum: Tuple[str, ...] = ('Others', 'Water_Proof', 'Vapour_Proof', 'Concrete', 'Wood_Timberproducts', 'Insulation', 'Masonry', 'Metal', 'Mortar', 'Plastics', 'Stone', 'Composite', 'Films', 'Render', 'Covering', 'Glas', 'Soil', 'air')
    xml_name: str = "groupkind"


class Materialtype(str):
    xs_type: str = "simpleType"
    xml_enum: Tuple[str, ...] = ('simple', 'btk', 'construction')
    xml_name: str = "materialtype"


class T2Uppercase(str):
    xs_type: str = "simpleType"
    xml_pattern:str = "[A-Z][A-Z]"
    xml_name: str = "T2Uppercase"


class TDateTime(float):
    xs_type: str = "simpleType"
    xml_name: str = "TDateTime"


class Guid(str):
    xs_type: str = "simpleType"
    xml_pattern:str = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    xml_name: str = "guid"


class Brackguid(str):
    xs_type: str = "simpleType"
    xml_pattern:str = "\{[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}\}"
    xml_name: str = "Brackguid"


class Boolean(int):
    xs_type: str = "simpleType"
    xml_pattern:str = "[0-1]"
    xml_name: str = "boolean"


class Mimetype(str):
    xs_type: str = "simpleType"
    xml_name: str = "mimetype"


class ISO639_1(T2Lowercase):
    xs_type: str = "simpleType"
    xml_enum: Tuple[str, ...] = ('aa', 'ab', 'af', 'am', 'ar', 'as', 'ay', 'az', 'ba', 'be', 'bg', 'bh', 'bi', 'bn', 'bo', 'br', 'ca', 'co', 'cs', 'cy', 'da', 'de', 'dz', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fj', 'fo', 'fr', 'fy', 'ga', 'gd', 'gl', 'gn', 'gu', 'ha', 'he', 'hi', 'hr', 'hu', 'hy', 'ia', 'ie', 'ik', 'id', 'is', 'it', 'iu', 'ja', 'jv', 'ka', 'kk', 'kl', 'km', 'kn', 'ko', 'ks', 'ku', 'ky', 'la', 'ln', 'lo', 'lt', 'lv', 'mg', 'mi', 'mk', 'ml', 'mn', 'mo', 'mr', 'ms', 'mt', 'my', 'na', 'ne', 'nl', 'no', 'oc', 'om', 'or', 'pa', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru', 'rw', 'sa', 'sd', 'sg', 'sh', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ug', 'uk', 'ur', 'uz', 'vi', 'vo', 'wo', 'xh', 'yi', 'yo', 'za', 'zh', 'zu')
    xml_name: str = "ISO639_1"


class ISO_3166_1_alpha_2(T2Uppercase):
    xs_type: str = "simpleType"
    xml_enum: Tuple[str, ...] = ('AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AN', 'AO', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AW', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BM', 'BN', 'BO', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CS', 'CU', 'CV', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'ST', 'SV', 'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW')
    xml_name: str = "ISO_3166_1_alpha_2"


class THexHash(str):
    ver: int
    xs_type: str = "complexType"
    xml_attributes: Tuple[str, ...] = ('ver',)
    xml_name: str = "THexHash"
    def __new__(cls, object, *args, **kwargs):
        obj = str.__new__(cls, object)
        for arg_name, arg_value in zip(['ver'], args):
            arg_name = arg_value
        for key, value in kwargs.items():
            if key == "object":
                continue
            setattr(obj, key, value)
        return obj


class TLocalizedString(str):
    xs_type: str = "complexType"
    lang: Optional[ISO639_1] = None
    xml_attributes: Tuple[str, ...] = ('lang',)
    xml_name: str = "TLocalizedString"
    def __new__(cls, object, *args, **kwargs):
        obj = str.__new__(cls, object)
        for arg_name, arg_value in zip(['lang'], args):
            arg_name = arg_value
        for key, value in kwargs.items():
            if key == "object":
                continue
            setattr(obj, key, value)
        return obj


class TCountryLocalizedString(TLocalizedString):
    xs_type: str = "complexType"
    lang: Optional[ISO639_1] = None
    country: Optional[ISO_3166_1_alpha_2] = None
    xml_attributes: Tuple[str, ...] = ('lang', 'country')
    xml_name: str = "TCountryLocalizedString"
    def __new__(cls, object, *args, **kwargs):
        obj = TLocalizedString.__new__(cls, object)
        for arg_name, arg_value in zip(['lang', 'country'], args):
            arg_name = arg_value
        for key, value in kwargs.items():
            if key == "object":
                continue
            setattr(obj, key, value)
        return obj


class TNamedString(str):
    name: str
    xs_type: str = "complexType"
    xml_attributes: Tuple[str, ...] = ('name',)
    xml_name: str = "TNamedString"
    def __new__(cls, object, *args, **kwargs):
        obj = str.__new__(cls, object)
        for arg_name, arg_value in zip(['name'], args):
            arg_name = arg_value
        for key, value in kwargs.items():
            if key == "object":
                continue
            setattr(obj, key, value)
        return obj


@dataclass
class Names:
    name: List[TCountryLocalizedString]
    xs_type: str = "element"
    xml_attributes: Tuple[str, ...] = ()
    xml_name = "names"
    xml_elements: Tuple[str, ...] = ('name',)


@dataclass
class Labels:
    label: List[TNamedString]
    xs_type: str = "element"
    xml_attributes: Tuple[str, ...] = ()
    xml_name = "labels"
    xml_elements: Tuple[str, ...] = ('label',)


@dataclass
class Country:
    sellingfrom: TDateTime
    xs_type: str = "element"
    name: Optional[ISO_3166_1_alpha_2] = None
    sellinguntil: Optional[TDateTime] = None
    xml_attributes: Tuple[str, ...] = ('name', 'sellingfrom', 'sellinguntil')
    xml_name = "country"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Countries:
    country: List[Country]
    xs_type: str = "element"
    xml_attributes: Tuple[str, ...] = ()
    xml_name = "countries"
    xml_elements: Tuple[str, ...] = ('country',)


@dataclass
class Explanations:
    explanation: List[TLocalizedString]
    xs_type: str = "element"
    xml_attributes: Tuple[str, ...] = ()
    xml_name = "explanations"
    xml_elements: Tuple[str, ...] = ('explanation',)


@dataclass
class Webinfo:
    href: str
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    lang: Optional[ISO639_1] = None
    mime: Optional[Mimetype] = None
    size: Optional[float] = None
    title: Optional[str] = None
    xml_attributes: Tuple[str, ...] = ('country', 'lang', 'mime', 'size', 'title', 'href')
    xml_name = "webinfo"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Webinfos:
    webinfo: List[Webinfo]
    xs_type: str = "element"
    xml_attributes: Tuple[str, ...] = ()
    xml_name = "webinfos"
    xml_elements: Tuple[str, ...] = ('webinfo',)


@dataclass
class Companyref:
    xs_type: str = "element"
    reftype: Optional[str] = None
    xml_attributes: Tuple[str, ...] = ('reftype',)
    xml_name = "companyref"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Companyrefs:
    companyref: List[Companyref]
    xs_type: str = "element"
    xml_attributes: Tuple[str, ...] = ()
    xml_name = "companyrefs"
    xml_elements: Tuple[str, ...] = ('companyref',)


@dataclass
class Information:
    names: Names
    xs_type: str = "element"
    group: Optional[Groupkind] = Groupkind("Others")
    wall: Optional[Boolean] = Boolean("0")
    roof: Optional[Boolean] = Boolean("0")
    floor: Optional[Boolean] = Boolean("0")
    door: Optional[Boolean] = Boolean("0")
    color: Optional[int] = None
    BrushStyle: Optional[int] = None
    xml_attributes: Tuple[str, ...] = ('group', 'wall', 'roof', 'floor', 'door', 'color', 'BrushStyle')
    labels: Optional[Labels] = None
    countries: Optional[Countries] = None
    explanations: Optional[Explanations] = None
    webinfos: Optional[Webinfos] = None
    companyrefs: Optional[Companyrefs] = None
    xml_name = "information"
    xml_elements: Tuple[str, ...] = ('names', 'labels', 'countries', 'explanations', 'webinfos', 'companyrefs')


@dataclass
class Geometry:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    thick: Optional[float] = None
    length: Optional[str] = None
    width: Optional[str] = None
    design: Optional[str] = None
    xml_attributes: Tuple[str, ...] = ('country', 'thick', 'length', 'width', 'design')
    xml_name = "geometry"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Thermal:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    lambda_value: Optional[float] = None
    lambda_value_dry: Optional[float] = None
    mu_min: Optional[float] = None
    mu_max: Optional[float] = None
    therm_capa: Optional[float] = None
    W80_coef: Optional[float] = None
    Wf_coef: Optional[float] = None
    A_coef: Optional[float] = None
    B_coef: Optional[float] = None
    Allwd_Moisture: Optional[float] = None
    xml_attributes: Tuple[str, ...] = ('country', 'lambda_value', 'lambda_value_dry', 'mu_min', 'mu_max', 'therm_capa', 'W80_coef', 'Wf_coef', 'A_coef', 'B_coef', 'Allwd_Moisture')
    xml_name = "thermal"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Physical:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    MinElas: Optional[float] = None
    MaxElas: Optional[float] = None
    ResCompMin: Optional[float] = None
    ResTractMin: Optional[float] = None
    density: Optional[float] = None
    T: Optional[str] = None
    CP: Optional[str] = None
    WS: Optional[str] = None
    Porosity: Optional[float] = None
    DS_TH: Optional[str] = None
    xml_attributes: Tuple[str, ...] = ('country', 'MinElas', 'MaxElas', 'ResCompMin', 'ResTractMin', 'density', 'T', 'CP', 'WS', 'Porosity', 'DS_TH')
    xml_name = "physical"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Security:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    FireComb: Optional[TFireComb] = None
    FireSmoke: Optional[TFireSmoke] = None
    FireResis: Optional[TFireResis] = None
    FireReact: Optional[TFireReact] = None
    Baustoffklasse: Optional[TFireDin4102] = None
    FireClass: Optional[str] = None
    xml_attributes: Tuple[str, ...] = ('country', 'FireComb', 'FireSmoke', 'FireResis', 'FireReact', 'Baustoffklasse', 'FireClass')
    xml_name = "security"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Acoustic:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    n125: Optional[float] = None
    n250: Optional[float] = None
    n500: Optional[float] = None
    n1000: Optional[float] = None
    n2000: Optional[float] = None
    n4000: Optional[float] = None
    free_space: Optional[float] = None
    SD: Optional[float] = None
    air_flow_resistivity: Optional[float] = None
    xml_attributes: Tuple[str, ...] = ('country', 'n125', 'n250', 'n500', 'n1000', 'n2000', 'n4000', 'free_space', 'SD', 'air_flow_resistivity')
    xml_name = "acoustic"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Other:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    Rademissivity: Optional[float] = None
    Radabsorp: Optional[float] = None
    usetemplimit: Optional[float] = None
    ProductCode: Optional[str] = None
    materialtype: Optional[str] = None
    TargetPrice: Optional[float] = None
    xml_attributes: Tuple[str, ...] = ('country', 'Rademissivity', 'Radabsorp', 'usetemplimit', 'ProductCode', 'materialtype', 'TargetPrice')
    xml_name = "other"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Lcia:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    UBP: Optional[float] = None
    NRE: Optional[float] = None
    GWP: Optional[float] = None
    CED: Optional[float] = None
    IPRIM: Optional[float] = None
    IENV: Optional[float] = None
    IECO: Optional[float] = None
    IECO12: Optional[float] = None
    KBOB_eq: Optional[Brackguid] = None
    xml_attributes: Tuple[str, ...] = ('country', 'UBP', 'NRE', 'GWP', 'CED', 'IPRIM', 'IENV', 'IECO', 'IECO12', 'KBOB_eq')
    xml_name = "lcia"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Lcaversion:
    id: str
    code: Brackguid
    xs_type: str = "element"
    xml_attributes: Tuple[str, ...] = ('id', 'code')
    xml_name = "lcaversion"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Lca:
    database: TLCADB
    xs_type: str = "element"
    luxInsulation: Optional[Guid] = None
    xml_attributes: Tuple[str, ...] = ('database', 'luxInsulation')
    lcaversion: Optional[List[Lcaversion]] = None
    xml_name = "lca"
    xml_elements: Tuple[str, ...] = ('lcaversion',)


@dataclass
class Emission:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    TVOC: Optional[float] = None
    Formaldehide: Optional[float] = None
    Ammonia: Optional[float] = None
    Carginogenic: Optional[float] = None
    xml_attributes: Tuple[str, ...] = ('country', 'TVOC', 'Formaldehide', 'Ammonia', 'Carginogenic')
    xml_name = "emission"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Layer:
    id: Guid
    xs_type: str = "element"
    aliases: Optional[str] = None
    displayorder: Optional[int] = None
    xml_attributes: Tuple[str, ...] = ('id', 'aliases', 'displayorder')
    geometry: Optional[List[Geometry]] = None
    thermal: Optional[List[Thermal]] = None
    physical: Optional[List[Physical]] = None
    security: Optional[List[Security]] = None
    acoustic: Optional[List[Acoustic]] = None
    other: Optional[List[Other]] = None
    lcia: Optional[List[Lcia]] = None
    lca: Optional[List[Lca]] = None
    emission: Optional[List[Emission]] = None
    xml_name = "layer"
    xml_elements: Tuple[str, ...] = ('geometry', 'thermal', 'physical', 'security', 'acoustic', 'other', 'lcia', 'lca', 'emission')


@dataclass
class Layers:
    layer: List[Layer]
    xs_type: str = "element"
    xml_attributes: Tuple[str, ...] = ()
    xml_name = "layers"
    xml_elements: Tuple[str, ...] = ('layer',)


@dataclass
class Vgeometry:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    thick: Optional[float] = None
    density: Optional[float] = None
    xml_attributes: Tuple[str, ...] = ('country', 'thick', 'density')
    xml_name = "vgeometry"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Vthermal:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    U_value_without: Optional[float] = None
    U_value_with: Optional[float] = None
    ETA1: Optional[float] = None
    ETA2: Optional[float] = None
    U24: Optional[float] = None
    CM1: Optional[float] = None
    CM2: Optional[float] = None
    metalcladding: Optional[Boolean] = Boolean("0")
    xml_attributes: Tuple[str, ...] = ('country', 'U_value_without', 'U_value_with', 'ETA1', 'ETA2', 'U24', 'CM1', 'CM2', 'metalcladding')
    xml_name = "vthermal"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Vacoustic:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    lang: Optional[ISO639_1] = None
    ExplainAcoustic: Optional[str] = None
    RwCalc: Optional[float] = None
    RwPrimeCalc: Optional[float] = None
    RwMesured: Optional[float] = None
    RwPrimeMesured: Optional[float] = None
    xml_attributes: Tuple[str, ...] = ('country', 'lang', 'ExplainAcoustic', 'RwCalc', 'RwPrimeCalc', 'RwMesured', 'RwPrimeMesured')
    xml_name = "vacoustic"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Vother:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    ProductCode: Optional[str] = None
    Rademissivity: Optional[float] = None
    Radabsorp: Optional[float] = None
    xml_attributes: Tuple[str, ...] = ('country', 'ProductCode', 'Rademissivity', 'Radabsorp')
    xml_name = "vother"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Vlcia:
    xs_type: str = "element"
    country: Optional[ISO_3166_1_alpha_2] = None
    UBP: Optional[float] = None
    NRE: Optional[float] = None
    GWP: Optional[float] = None
    CED: Optional[float] = None
    IPRIM: Optional[float] = None
    IENV: Optional[float] = None
    IECO: Optional[float] = None
    IECO12: Optional[float] = None
    KBOB_eq: Optional[Brackguid] = None
    xml_attributes: Tuple[str, ...] = ('country', 'UBP', 'NRE', 'GWP', 'CED', 'IPRIM', 'IENV', 'IECO', 'IECO12', 'KBOB_eq')
    xml_name = "vlcia"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Vlca:
    database: TLCADB
    xs_type: str = "element"
    luxInsulation: Optional[Guid] = None
    xml_attributes: Tuple[str, ...] = ('database', 'luxInsulation')
    lcaversion: Optional[List[Lcaversion]] = None
    xml_name = "vlca"
    xml_elements: Tuple[str, ...] = ('lcaversion',)


@dataclass
class Variation:
    id: Guid
    vgeometry: List[Vgeometry]
    vthermal: List[Vthermal]
    xs_type: str = "element"
    displayorder: Optional[int] = None
    xml_attributes: Tuple[str, ...] = ('id', 'displayorder')
    vacoustic: Optional[List[Vacoustic]] = None
    vother: Optional[List[Vother]] = None
    vlcia: Optional[List[Vlcia]] = None
    vlca: Optional[List[Vlca]] = None
    xml_name = "variation"
    xml_elements: Tuple[str, ...] = ('vgeometry', 'vthermal', 'vacoustic', 'vother', 'vlcia', 'vlca')


@dataclass
class Variations:
    variation: List[Variation]
    xs_type: str = "element"
    xml_attributes: Tuple[str, ...] = ()
    xml_name = "variations"
    xml_elements: Tuple[str, ...] = ('variation',)


@dataclass
class Construction:
    xs_type: str = "element"
    source: Optional[str] = None
    consref: Optional[str] = None
    xml_attributes: Tuple[str, ...] = ('source', 'consref')
    xml_name = "construction"
    xml_elements: Tuple[str, ...] = ()


@dataclass
class Material:
    id: Guid
    type: Materialtype
    information: Information
    xs_type: str = "element"
    readonly: Optional[Boolean] = Boolean("1")
    xml_attributes: Tuple[str, ...] = ('id', 'type', 'readonly')
    layers: Optional[Layers] = None
    variations: Optional[Variations] = None
    construction: Optional[Construction] = None
    xml_name = "material"
    xml_elements: Tuple[str, ...] = ('information', 'layers', 'variations', 'construction')


@dataclass
class Materials:
    company: str
    companyid: Guid
    ver: int
    crd: TDateTime
    verXML: int
    material: List[Material]
    sig: THexHash
    publickey: THexHash
    xs_type: str = "element"
    SchemaLocation: Optional[str] = None
    xml_attributes: Tuple[str, ...] = ('company', 'companyid', 'ver', 'crd', 'verXML', 'SchemaLocation')
    xml_name = "materials"
    xml_elements: Tuple[str, ...] = ('material', 'sig', 'publickey')

