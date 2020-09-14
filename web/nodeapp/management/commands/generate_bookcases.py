from django.core.management.base import BaseCommand

import os
import pickle

from nodeapp.bookcases import load_bookcases

class Command(BaseCommand):
    def handle(self, *args, **options):
        companies = [13284,13373,13510,14849,15701,17536,19335,19887,23695,11496,11497,11498,11502,11530,11532,11553,11554,11569,11578,11579,11581,11582,11589,11590,11594,11603,11617,11623,11659,11662,11671,11677,11691,11728,11731,11737,11745,11766,11775,11813,11838,11867,11873,11904,11932,11934,11936,11942,11945,11948,11949,11990,11994,12026,12027,12028,12036,12046,12050,12051,12072,12095,12099,12102,12133,12140,12151,12183,12197,12219,12256,12261,12271,12293,12296,12299,12335,12351,12402,12419,12438,12447,12469,12491,12493,12494,12497,12545,12561,12592,12604,12631,12633,12651,12655,12680,12686,12692,12695,12702,12707,12713,12719,12748,12766,12767,12770,12786,12799,12811,12824,12834,12854,12870,12875,12878,12899,12929,12960,12972,12982,12995,13042,13047,13049,13080,13113,13115,13121,13129,13134,13135,13147,13164,13167,13173,13192,13197,13201,13216,13220,13251,13258,13284,13287,13292,13297,13304,13306,13311,13342,13355,13365,13368,13373,13376,13387,13396,13419,13438,13441,13444,13449,13464,13478,13493,13496,13510,13532,13572,13598,13606,13615,13617,13618,13627,13630,13660,13663,13667,13669,13680,13681,13709,13711,13727,13728,13729,13731,13765,13800,13801,13809,13821,13829,13843,13865,13874,13891,13906,13926,13934,13940,13941,13945,13951,13957,13961,13993,14025,14033,14039,14050,14107,14132,14146,14158,14181,14229,14297,14317,14330,14339,14354,14383,14438,14467,14473,14476,14481,14497,14499,14500,14501,14503,14516,14521,14527,14546,14576,14632,14641,14656,14661,14663,14668,14695,14725,14728,14755,14767,14808,14814,14816,14817,14830,14849,14864,14866,14873,14883,14890,14905,14906,14928,14932,14953,14967,14983,14984,15006,15027,15028,15029,15052,15062,15067,15121,15126,15170,15176,15188,15241,15245,15250,15287,15293,15304,15305,15307,15329,15332,15341,15356,15359,15360,15361,15386,15399,15452,15498,15500,15526,15527,15543,15562,15584,15594,15595,15618,15656,15668,15681,15682,15692,15701,15704,15718,15719,15755,15764,15815,15816,15822,15824,15893,15894,15908,15911,15951,15954,15959,15971,15982,15983,16011,16018,16024,16051,16072,16099,16104,16127,16153,16154,16159,16186,16192,16211,16219,16236,16253,16258,16265,16266,16277,16307,16324,16329,16367,16368,16369,16372,16389,16390,16428,16430,16446,16452,16454,16462,16476,16491,16492,16497,16515,16526,16537,16541,16544,16551,16567,16590,16607,16625,16634,16644,16645,16649,16658,16659,16662,16678,16687,16695,16714,16737,16753,16768,16773,16777,16783,16791,16793,16797,16806,16809,16818,16830,16838,16872,16874,16877,16880,16885,16886,16905,16914,16984,16987,16988,16990,17034,17036,17037,17054,17057,17070,17092,17102,17104,17105,17106,17107,17115,17119,17148,17149,17184,17186,17192,17194,17199,17202,17204,17221,17222,17230,17236,17240,17261,17268,17270,17293,17298,17300,17301,17305,17318,17353,17375,17399,17404,17410,17426,17430,17451,17472,17480,17536,17581,17606,17628,17642,17662,17669,17672,17674,17676,17687,17703,17706,17730,17734,17759,17772,17783,17800,17804,17812,17835,17836,17842,17860,17863,17869,17876,17898,17932,17946,17949,17962,17965,17987,17991,17999,18002,18031,18044,18047,18066,18072,18096,18100,18115,18118,18142,18145,18148,18159,18168,18171,18175,18179,18185,18195,18197,18198,18199,18200,18204,18205,18206,18209,18244,18251,18254,18257,18260,18292,18323,18329,18353,18361,18377,18384,18387,18412,18438,18455,18468,18472,18478,18480,18497,18501,18538,18545,18552,18556,18567,18570,18580,18589,18597,18618,18631,18644,18650,18664,18665,18676,18699,18702,18712,18714,18734,18736,18741,18746,18765,18791,18835,18838,18850,18855,18859,18887,18896,18904,18945,18946,18958,18964,18993,18995,18997,18999,19010,19012,19015,19018,19042,19046,19057,19067,19068,19072,19080,19125,19150,19153,19160,19188,19206,19209,19211,19217,19225,19230,19238,19276,19277,19278,19279,19280,19282,19328,19330,19331,19335,19339,19347,19356,19359,19369,19380,19388,19411,19419,19440,19494,19536,19541,19544,19561,19562,19579,19676,19678,19691,19714,19720,19722,19723,19726,19738,19771,19772,19783,19789,19822,19823,19868,19877,19883,19885,19887,19893,19913,19916,19917,19921,19926,19937,19939,19942,19950,19951,19977,19989,20010,20016,20043,20057,20061,20071,20072,20084,20085,20091,20130,20133,20155,20176,20186,20211,20218,20219,20234,20289,20299,20305,20331,20335,20363,20364,20380,20384,20393,20401,20418,20436,20441,20465,20471,20475,20478,20480,20497,20499,20531,20575,20588,20600,20602,20611,20627,20631,20638,20647,20652,20655,20665,20666,20682,20696,20715,20724,20725,20745,20752,20753,20766,20804,20826,20849,20850,20851,20853,20885,20903,20912,20917,20930,20936,20937,20953,20954,20965,20971,20990,20995,21002,21030,21032,21040,21045,21055,21086,21139,21156,21172,21189,21216,21245,21249,21270,21284,21305,21315,21332,21333,21345,21347,21371,21378,21381,21404,21417,21435,21454,21458,21495,21496,21554,21621,21623,21705,21741,21757,21758,21765,21772,21778,21794,21812,21832,21836,21839,21843,21887,21894,21895,21906,21907,21910,21920,21924,21929,21935,21942,21950,21964,21974,22011,22021,22038,22040,22064,22092,22093,22114,22115,22121,22132,22139,22142,22147,22151,22159,22186,22215,22236,22239,22244,22270,22271,22326,22351,22364,22412,22416,22418,22427,22435,22478,22481,22496,22510,22520,22599,22620,22625,22626,22634,22635,22640,22642,22650,22653,22665,22670,22676,22678,22710,22723,22725,22728,22729,22745,22749,22758,22765,22766,22776,22785,22793,22804,22838,22845,22860,22874,22931,22934,22947,22953,22980,22996,23009,23011,23031,23037,23085,23117,23124,23133,23138,23145,23150,23191,23194,23198,23200,23206,23207,23230,23244,23257,23280,23309,23344,23351,23358,23366,23368,23371,23387,23390,23398,23412,23426,23434,23435,23436,23438,23476,23486,23493,23494,23510,23518,23519,23543,23545,23552,23587,23590,23595,23619,23626,23654,23656,23657,23661,23664,23668,23684,23693,23695,23698,23706,23708,23715,23726,23734,23735,23737,23761,23767,23792,23793,23795,23799,23809,23814,23821,23825,23854,23858,23860,23864,23869,23870,23871,23890,23893,23909,23910,23928,23950,23964,23968,23985,23997,24003,24038,24069,24075,24088,24096,24103,24108,24128,24142,24155,24163,24178,24185,24190,24195,26569,28266,28761,29314,29933,30101,30780,31242,36468,38005,38064,38569,39890,40159,40508,43667,43848,45998]
        bc_companies, bookcase_classic, bookcase_query, bookcase_classic_not_filtered, bookcase_query_not_filtered \
            = load_bookcases('', companies)

        if not os.path.exists('temp'):
            os.mkdir('temp')

        with open(os.path.join('temp', 'static.pickle') , 'wb') as handle:
            pickle.dump(bookcase_classic, handle, protocol=3)

        with open(os.path.join('temp', 'dynamic.pickle') , 'wb') as handle:
            pickle.dump(bookcase_query, handle, protocol=3)