from enum import Enum
from collections import namedtuple

RegionProps = namedtuple('RegionProps', 'endpoint friendly_name')

class Region(Enum):
    BRAZIL = RegionProps('br1', 'Brazil')
    EUNE = RegionProps('eun1', 'Europe Nordic & East')
    EUW = RegionProps('euw1', 'Europe West')
    JP = RegionProps('jp1', 'Japan')
    KR = RegionProps('kr', 'Korea')
    LATIN1 = RegionProps('la1', 'Latin America North')
    LATIN2 = RegionProps('la2', 'Latin America South')
    NA = RegionProps('na1', 'North America')
    OC = RegionProps('oc1', 'Oceania')
    TR = RegionProps('tr1', 'Turkey')
    RU = RegionProps('ru', 'Russia')
    PH = RegionProps('ph2', 'The Philippines')
    SG = RegionProps('sg2', 'Singapore, Malaysia, & Indonesia')
    TH = RegionProps('th2', 'Thailand')
    TW = RegionProps('tw2', 'Taiwan, Hong Kong, and Macao')
    VN = RegionProps('vn2', 'Vietnam')

class Product(Enum):
    LeagueOfLegends = 'lol'

class Queue(Enum):
    RankedFlex = 'RANKED_FLEX_SR'
    RankedSolo = 'RANKED_SOLO_5x5'
