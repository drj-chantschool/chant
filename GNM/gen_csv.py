import csv

PART_MAP = {'in': 1, 'of': 8, 'co': 9}

resolved = {
    'in-excelso-throno': 20, 'dominus-secus-mare': 693, 'venite-adoremus': 450,
    'dominus-fortitudo': 522, 'dum-clamarem': 299, 'ego-autem-cum-justitia': 830,
    'deus-in-loco-sancto': 1026, 'sitientes': 776, 'justus-es': 1284,
    'in-voluntate': 1047, 'si-iniquitates': 8690, 'ne-derelinquas': 7759,
    'dicit-dominus-ego': 3923, 'loquetur-dominus': 271, 'invocabit-me': 327,
    'redemisti-nos': 7096, 'repleatur-os': 557, 'mihi-autem-nimis': 5848,
    'in-nomine-jesu': 18080, 'statuit': 456, 'jubilate-deo-universa': 937,
    'perfice-gressus': 265, 'benedicam-domino': 11077, 'populum-humilem': 1080,
    'precatus-est': 325, 'in-te-speravi': 967, 'exspectans-exspectavi': 13717,
    'oravi-deum': 652, 'vir-erat': 1363, 'meditabor': 810,
    'domine-vivifica': 109, 'domine-ad-adjuvandum': 731, 'super-flumina': 812,
    'notas-mihi': 6934, 'laetabimur': 1296, 'dicit-andreas': 1021,
    'multitudo-languentium': 1267, 'comedite-pinguia': 496, 'quicumque-fecerit': 957,
    'unam-petii': 574, 'quod-dico-vobis': 1002, 'passer-invenit': 1090,
    'ecce-sto': 164, 'simile-est': 6271, 'petite': 5618,
    'panem-de-caelo': 388, 'beatus-servus': 1154, 'domine-memorabor': 1318,
    'dico-vobis': 1058, 'hoc-corpus': 726, 'in-salutari': 1290,
    'dico-autem-vobis': 699, 'fidelis-servus': 3902,
    'amen-dico-vobis-quidquid': 592, 'jerusalem-quae-aedificatur': 13460,
    'memento-verbi': 696, 'populus-acquisitionis': 1219, 'panis-quem-ego': 782,
    'feci-judicium': 844, 'qui-meditabitur': 582, 'manducaverunt': 677,
    'benedicite-omnes-angeli': 1127,
    # Disambiguated by local_chant
    'omnis-terra': 13, 'adorate-deum': 1123, 'laetetur-cor': 864,
    'suscepimus': 1781, 'ecce-deus': 1357, 'exsultate-deo': 1323,
    'deus-in-adjutorium': 501, 'inclina-domine': 1165, 'da-pacem': 172,
    'salus-populi': 389, 'ego-clamavi': 558, 'misereris-omnium': 533,
    'intret-oratio': 238, 'verba-mea': 1248, 'omnia-quae': 1056,
    'victricem': 1332, 'deus-dum-egredereris': 822, 'jubilate-deo': 536,
    'misericordia-domini': 135, 'venite-benedicti': 997,
    'signum-magnum': 23, 'in-medio-ecclesiae': 233, 'benedicite-dominum': 985,
    'jubilate-deo-omnis': 718, 'dextera-domini': 47, 'bonum-est-confiteri': 1194,
    'ad-te-domine': 962, 'justitiae-domini': 591, 'exaltabo-te': 648,
    'sanctificavit': 838, 'domine-in-auxilium': 993, 'si-ambulavero': 616,
    'recordare-mei': 67, 'benedic-anima-mea': 1359, 'gressus-meos': 1099,
    'in-die-solemnitatis': 1129, 'lauda-anima': 668, 'deus-deus-meus': 924,
    'veritas-mea': 630, 'constitues-eos': 1319, 'in-omnem-terram': 3360,
    'majorem-caritatem': 401, 'immittet-angelus': 747,
    'venite-post-me': 552, 'ego-vos-elegi': 470, 'mirabantur': 1148,
    'illumina-faciem': 640, 'beati-mundo-corde': 345, 'introibo': 554,
    'mense-septimo': 1149, 'circuibo': 1079, 'qui-vult-venire': 89,
    'gustate': 1203, 'qui-manducat': 798, 'acceptabis': 1221,
    'optimam-partem': 3316, 'honora-dominum': 1145, 'panis-quem': 782,
    'de-fructu': 1245, 'domine-quinque-talenta': 383, 'vovete': 1134,
    'tollite-hostias': 404, 'tu-mandasti': 479, 'beata-viscera': 160,
    'aufer-a-me': 828, 'domine-dominus-noster': 998, 'dominus-regit-me': 278,
    'quinque-prudentes': 3388, 'domus-mea': 43, 'laudate-dominum': 322,
    'spiritus-ubi-vult': 6930, 'tanto-tempore': 13575,
    'joseph-fili-david': 139, 'mitte-manum': 589, 'beatam-me-dicent': 286,
    'de-profundis': 986, 'respice-domine': 691, 'angelus-domini': 789,
    'assumpta-est-maria': 3317,
    # NOT_FOUND resolved
    'miserere-mihi-ad-te': 335, 'gaudeamus-agathae': 1183,
    'gaudeamus-mariae-assumptione': 3312, 'mitte-manum-alleluia': 953,
    'vos-qui-secuti-estis-me': 1028,
    'vos-qui-secuti-estis-me-dicit-dominus': 97,
    'afferentur-post-eam': 768,
    # Context-dependent
    'justus-ut-palma-in': 3816, 'justus-ut-palma-of': 3841,
    'cantate-domino-co': 579, 'cantate-domino-in': 42,
    'video-caelos': 7087,
}

needs_user = {
    'exaudi-domine': '13504(mode1) or 13741(mode4) — no English chant for either',
    'stetit-angelus': '14086(mode1) or 15430(mode4) — no English chant for either',
    'quasi-modo-geniti': '25 — exists (in. mode 6) but no English chant uploaded',
    'de-ventre-matris-meae': '659 — exists (in. mode 1) but no English chant uploaded',
    'accipite-iucunditatem': '13844(mode4) or 1278(mode4) or 6064(mode8) — no English chant',
    'simon-ioannis': '846 — exists (co. mode 6) but no English chant uploaded',
    'surrexit-dominus': '121 — Surrexit Dominus et apparuit (co. mode 6) no English chant',
    'ego-sum-pastor-bonus': 'no co. version found; 8784 is in. mode 3',
    'laetatur-cor': 'NO chant_group found (distinct from laetetur-cor 864)',
    'dicit-dominus-implete-hydrias': 'NO chant_group found',
    'quinque-prudentes-virgines': '3388? (quinque-prudentes co. mode 5) — same chant?',
    'in-conspectu-angelorum': '662(of. mode 1) — no co. version found; used as co in tex',
}

rows = []

def add(src, slug, part, season, subseason, wknum, seq, cycle_sun, cycle_wk, notes=''):
    if slug == 'justus-ut-palma' and part == 'in':
        cg_id, status = resolved.get('justus-ut-palma-in', ''), 'RESOLVED'
    elif slug == 'justus-ut-palma' and part == 'of':
        cg_id, status = resolved.get('justus-ut-palma-of', ''), 'RESOLVED'
    elif slug == 'cantate-domino' and part == 'co':
        cg_id, status = resolved.get('cantate-domino-co', ''), 'RESOLVED'
    elif slug == 'cantate-domino' and part == 'in':
        cg_id, status = resolved.get('cantate-domino-in', ''), 'RESOLVED'
    elif slug in resolved:
        cg_id, status = resolved[slug], 'RESOLVED'
    elif slug in needs_user:
        cg_id, status = '', 'NEEDS_INPUT'
        notes = (notes + '; ' + needs_user[slug]) if notes else needs_user[slug]
    else:
        cg_id, status = '', 'UNKNOWN'

    rows.append({
        'source_file': src, 'slug': slug, 'part': part, 'part_id': PART_MAP[part],
        'season': season or '', 'subseason': subseason or '',
        'wknum': '' if wknum is None else wknum,
        'seq': '' if seq is None else seq,
        'cycle_sun': '' if cycle_sun is None else cycle_sun,
        'cycle_wk': '' if cycle_wk is None else cycle_wk,
        'chant_group_id': cg_id, 'status': status, 'notes': notes,
    })

# ===== OT =====
# Week 1
add('GNM-01-OT','in-excelso-throno','in','OT','OT',1,None,None,None,'all days')
add('GNM-01-OT','jubilate-deo-omnis','of','OT','OT',1,None,None,None,'all days')
add('GNM-01-OT','notas-mihi','co','OT','OT',1,None,None,None,'all days')
add('GNM-01-OT','venite-post-me','co','OT','OT',1,2,None,None,'Mon if Baptism not on Sun')
# Week 2
add('GNM-02-OT','omnis-terra','in','OT','OT',2,None,None,None,'all days')
add('GNM-02-OT','jubilate-deo-universa','of','OT','OT',2,None,None,None,'all days')
add('GNM-02-OT','laetabimur','co','OT','OT',2,None,None,None,'default co')
add('GNM-02-OT','dicit-andreas','co','OT','OT',2,1,2,None,'Sunday B')
add('GNM-02-OT','dicit-dominus-implete-hydrias','co','OT','OT',2,1,0,None,'Sunday C')
add('GNM-02-OT','multitudo-languentium','co','OT','OT',2,5,None,None,'Thursday')
add('GNM-02-OT','ego-vos-elegi','co','OT','OT',2,6,None,None,'Friday')
# Week 3
add('GNM-03-OT','adorate-deum','in','OT','OT',3,None,None,None,'default in')
add('GNM-03-OT','dominus-secus-mare','in','OT','OT',3,1,1,None,'Sunday A')
add('GNM-03-OT','dominus-secus-mare','in','OT','OT',3,1,2,None,'Sunday B')
add('GNM-03-OT','dextera-domini','of','OT','OT',3,None,None,None,'all days')
add('GNM-03-OT','mirabantur','co','OT','OT',3,None,None,None,'default co')
add('GNM-03-OT','venite-post-me','co','OT','OT',3,1,1,None,'Sunday A')
add('GNM-03-OT','venite-post-me','co','OT','OT',3,1,2,None,'Sunday B')
add('GNM-03-OT','comedite-pinguia','co','OT','OT',3,1,0,None,'Sunday C')
add('GNM-03-OT','quicumque-fecerit','co','OT','OT',3,3,None,None,'Tuesday')
# Week 4
add('GNM-04-OT','laetetur-cor','in','OT','OT',4,None,None,None,'all days')
add('GNM-04-OT','bonum-est-confiteri','of','OT','OT',4,None,None,None,'all days')
add('GNM-04-OT','illumina-faciem','co','OT','OT',4,None,None,None,'default co')
add('GNM-04-OT','beati-mundo-corde','co','OT','OT',4,1,1,None,'Sunday A')
# Week 5
add('GNM-05-OT','venite-adoremus','in','OT','OT',5,None,None,None,'all days')
add('GNM-05-OT','perfice-gressus','of','OT','OT',5,None,None,None,'all days')
add('GNM-05-OT','introibo','co','OT','OT',5,None,None,None,'default co')
add('GNM-05-OT','multitudo-languentium','co','OT','OT',5,1,2,None,'Sunday B')
add('GNM-05-OT','multitudo-languentium','co','OT','OT',5,2,None,1,'Monday Yr I')
add('GNM-05-OT','mense-septimo','co','OT','OT',5,2,None,0,'Monday Yr II')
# Week 11
add('GNM-11-OT','exaudi-domine','in','OT','OT',11,None,None,None,'old-format file; user: which mode?')
add('GNM-11-OT','benedicam-domino','of','OT','OT',11,None,None,None,'all days')
add('GNM-11-OT','unam-petii','co','OT','OT',11,None,None,None,'all days')
# Week 12
add('GNM-12-OT','dominus-fortitudo','in','OT','OT',12,None,None,None,'all days')
add('GNM-12-OT','perfice-gressus','of','OT','OT',12,None,None,None,'all days')
add('GNM-12-OT','circuibo','co','OT','OT',12,None,None,None,'default co')
add('GNM-12-OT','quod-dico-vobis','co','OT','OT',12,1,1,None,'Sunday A')
add('GNM-12-OT','qui-vult-venire','co','OT','OT',12,1,0,None,'Sunday C')
# Week 14
add('GNM-14-OT','suscepimus','in','OT','OT',14,None,None,None,'all days')
add('GNM-14-OT','populum-humilem','of','OT','OT',14,None,None,None,'all days')
add('GNM-14-OT','gustate','co','OT','OT',14,None,None,None,'all days')
# Week 15
add('GNM-15-OT','dum-clamarem','in','OT','OT',15,None,None,None,'option 1')
add('GNM-15-OT','ego-autem-cum-justitia','in','OT','OT',15,None,None,None,'option 2 (or)')
add('GNM-15-OT','ad-te-domine','of','OT','OT',15,None,None,None,'all days')
add('GNM-15-OT','qui-manducat','co','OT','OT',15,None,None,None,'default co')
add('GNM-15-OT','passer-invenit','co','OT','OT',15,None,None,None,'or')
# Week 16
add('GNM-16-OT','ecce-deus','in','OT','OT',16,None,None,None,'all days')
add('GNM-16-OT','justitiae-domini','of','OT','OT',16,None,None,None,'all days')
add('GNM-16-OT','acceptabis','co','OT','OT',16,None,None,None,'default co')
add('GNM-16-OT','optimam-partem','co','OT','OT',16,1,0,None,'Sunday C')
add('GNM-16-OT','ecce-sto','co','OT','OT',16,None,None,None,'listed after optimam-partem; user: which days?')
# Week 17
add('GNM-17-OT','deus-in-loco-sancto','in','OT','OT',17,None,None,None,'default in')
add('GNM-17-OT','exsultate-deo','in','OT','OT',17,6,None,1,'Friday Yr I')
add('GNM-17-OT','exaltabo-te','of','OT','OT',17,None,None,None,'all days')
add('GNM-17-OT','honora-dominum','co','OT','OT',17,None,None,None,'default co')
add('GNM-17-OT','simile-est','co','OT','OT',17,1,1,None,'Sunday A')
add('GNM-17-OT','petite','co','OT','OT',17,1,0,None,'Sunday C')
# Week 18
add('GNM-18-OT','deus-in-adjutorium','in','OT','OT',18,None,None,None,'default in')
add('GNM-18-OT','sitientes','in','OT','OT',18,1,1,None,'Sunday A')
add('GNM-18-OT','precatus-est','of','OT','OT',18,None,None,None,'default of')
add('GNM-18-OT','sanctificavit','of','OT','OT',18,1,0,None,'Sunday C')
add('GNM-18-OT','panem-de-caelo','co','OT','OT',18,None,None,None,'default co')
add('GNM-18-OT','qui-vult-venire','co','OT','OT',18,6,None,None,'Friday')
# Week 19
add('GNM-19-OT','respice-domine','in','OT','OT',19,None,None,None,'all days')
add('GNM-19-OT','in-te-speravi','of','OT','OT',19,None,None,None,'all days')
add('GNM-19-OT','panis-quem','co','OT','OT',19,None,None,None,'default co')
add('GNM-19-OT','beatus-servus','co','OT','OT',19,None,None,None,'or')
# Week 21
add('GNM-21-OT','inclina-domine','in','OT','OT',21,None,None,None,'all days')
add('GNM-21-OT','exspectans-exspectavi','of','OT','OT',21,None,None,None,'all days')
add('GNM-21-OT','de-fructu','co','OT','OT',21,None,None,None,'default co')
add('GNM-21-OT','qui-manducat','co','OT','OT',21,None,None,None,'or')
add('GNM-21-OT','beatus-servus','co','OT','OT',21,5,None,None,'Thursday')
add('GNM-21-OT','quinque-prudentes-virgines','co','OT','OT',21,6,None,None,'Friday')
add('GNM-21-OT','domine-quinque-talenta','co','OT','OT',21,7,None,None,'Saturday')
# Week 22
add('GNM-22-OT','miserere-mihi-ad-te','in','OT','OT',22,None,None,None,'all days')
add('GNM-22-OT','domine-in-auxilium','of','OT','OT',22,None,None,None,'all days')
add('GNM-22-OT','domine-memorabor','co','OT','OT',22,None,None,None,'default co')
add('GNM-22-OT','qui-vult-venire','co','OT','OT',22,1,1,None,'Sunday A')
add('GNM-22-OT','mirabantur','co','OT','OT',22,2,None,None,'Mondays')
add('GNM-22-OT','multitudo-languentium','co','OT','OT',22,4,None,None,'Wednesdays')
# Week 23
add('GNM-23-OT','justus-es','in','OT','OT',23,None,None,None,'all days')
add('GNM-23-OT','oravi-deum','of','OT','OT',23,None,None,None,'all days')
add('GNM-23-OT','vovete','co','OT','OT',23,None,None,None,'default co')
add('GNM-23-OT','multitudo-languentium','co','OT','OT',23,3,None,None,'Tuesdays')
# Week 24
add('GNM-24-OT','da-pacem','in','OT','OT',24,None,None,None,'all days')
add('GNM-24-OT','sanctificavit','of','OT','OT',24,None,None,None,'default of')
add('GNM-24-OT','precatus-est','of','OT','OT',24,1,0,None,'Sunday C')
add('GNM-24-OT','tollite-hostias','co','OT','OT',24,None,None,None,'default co')
add('GNM-24-OT','qui-vult-venire','co','OT','OT',24,1,2,None,'Sunday B')
add('GNM-24-OT','dico-vobis','co','OT','OT',24,1,0,None,'Sunday C')
add('GNM-24-OT','hoc-corpus','co','OT','OT',24,2,None,0,'Monday Yr II')
# Week 25
add('GNM-25-OT','salus-populi','in','OT','OT',25,None,None,None,'all days')
add('GNM-25-OT','si-ambulavero','of','OT','OT',25,None,None,None,'all days')
add('GNM-25-OT','tu-mandasti','co','OT','OT',25,None,None,None,'all days')
# Week 26
add('GNM-26-OT','dum-clamarem','in','OT','OT',26,None,None,None,'option 1')
add('GNM-26-OT','ego-autem-cum-justitia','in','OT','OT',26,None,None,None,'option 2 (or)')
add('GNM-26-OT','ad-te-domine','of','OT','OT',26,None,None,None,'all days')
add('GNM-26-OT','qui-manducat','co','OT','OT',26,None,None,None,'default co')
add('GNM-26-OT','passer-invenit','co','OT','OT',26,None,None,None,'or')
# Week 27
add('GNM-27-OT','in-voluntate','in','OT','OT',27,None,None,None,'default in')
add('GNM-27-OT','de-ventre-matris-meae','in','OT','OT',27,3,None,0,'ad libitum Tue Yr II')
add('GNM-27-OT','vir-erat','of','OT','OT',27,None,None,None,'all days')
add('GNM-27-OT','in-salutari','co','OT','OT',27,None,None,None,'default co')
add('GNM-27-OT','optimam-partem','co','OT','OT',27,3,None,None,'Tuesdays')
add('GNM-27-OT','petite','co','OT','OT',27,5,None,None,'Thursdays')
add('GNM-27-OT','beata-viscera','co','OT','OT',27,7,None,None,'Saturdays')
# Week 28
add('GNM-28-OT','si-iniquitates','in','OT','OT',28,None,None,None,'all days')
add('GNM-28-OT','recordare-mei','of','OT','OT',28,None,None,None,'all days')
add('GNM-28-OT','aufer-a-me','co','OT','OT',28,None,None,None,'default co')
add('GNM-28-OT','dico-autem-vobis','co','OT','OT',28,None,None,None,'or')
# Week 29
add('GNM-29-OT','ego-clamavi','in','OT','OT',29,None,None,None,'all days')
add('GNM-29-OT','meditabor','of','OT','OT',29,None,None,None,'all days')
add('GNM-29-OT','domine-dominus-noster','co','OT','OT',29,None,None,None,'default co')
add('GNM-29-OT','beatus-servus','co','OT','OT',29,3,None,None,'Tuesday')
add('GNM-29-OT','fidelis-servus','co','OT','OT',29,4,None,None,'Wednesday')
# Week 30
add('GNM-30-OT','laetatur-cor','in','OT','OT',30,None,None,None,'')
add('GNM-30-OT','domine-vivifica','of','OT','OT',30,None,None,None,'all days')
add('GNM-30-OT','laetabimur','co','OT','OT',30,None,None,None,'all days')
# Week 31
add('GNM-31-OT','ne-derelinquas','in','OT','OT',31,None,None,None,'default in')
add('GNM-31-OT','misereris-omnium','in','OT','OT',31,1,0,None,'Sunday C')
add('GNM-31-OT','benedic-anima-mea','of','OT','OT',31,None,None,None,'all days')
add('GNM-31-OT','notas-mihi','co','OT','OT',31,None,None,None,'default co')
add('GNM-31-OT','dico-vobis','co','OT','OT',31,5,None,None,'Thursdays (optional)')
# Week 32
add('GNM-32-OT','intret-oratio','in','OT','OT',32,None,None,None,'all days')
add('GNM-32-OT','gressus-meos','of','OT','OT',32,None,None,None,'all days')
add('GNM-32-OT','dominus-regit-me','co','OT','OT',32,None,None,None,'default co')
add('GNM-32-OT','quinque-prudentes','co','OT','OT',32,1,1,None,'Sunday A')
# Week 33
add('GNM-33-OT','dicit-dominus-ego','in','OT','OT',33,None,None,None,'all days')
add('GNM-33-OT','de-profundis','of','OT','OT',33,None,None,None,'all days')
add('GNM-33-OT','amen-dico-vobis-quidquid','co','OT','OT',33,None,None,None,'default co')
add('GNM-33-OT','domine-quinque-talenta','co','OT','OT',33,1,1,None,'Sunday A')
add('GNM-33-OT','domine-quinque-talenta','co','OT','OT',33,4,None,None,'Wednesdays')
add('GNM-33-OT','domus-mea','co','OT','OT',33,6,None,None,'Fridays')
# Week 34
add('GNM-34-OT','loquetur-dominus','in','OT','OT',34,None,None,None,'weekdays only (Sun=Christ the King)')
add('GNM-34-OT','bonum-est-confiteri','of','OT','OT',34,None,None,None,'weekdays only')
add('GNM-34-OT','jerusalem-quae-aedificatur','co','OT','OT',34,None,None,None,'default co')
add('GNM-34-OT','laudate-dominum','co','OT','OT',34,None,None,None,'or')

# ===== LENT =====
# TQ-0 (Ash Wed week)
add('GNM-TQ-0','dum-clamarem','in','TQ','LENT',0,5,None,None,'Thu after Ash Wed')
add('GNM-TQ-0','ad-te-domine','of','TQ','LENT',0,5,None,None,'Thu after Ash Wed')
add('GNM-TQ-0','qui-vult-venire','co','TQ','LENT',0,5,None,None,'Thu after Ash Wed')
add('GNM-TQ-0','acceptabis','co','TQ','LENT',0,5,None,None,'traditional option')
# TQ-1
add('GNM-TQ-1','invocabit-me','in','TQ','LENT',1,1,None,None,'1st Sunday')
add('GNM-TQ-1','verba-mea','in','TQ','LENT',1,5,None,None,'Thursday')
add('GNM-TQ-1','recordare-mei','of','TQ','LENT',1,5,None,None,'Thursday')
add('GNM-TQ-1','petite','co','TQ','LENT',1,5,None,None,'Thursday')
add('GNM-TQ-1','acceptabis','co','TQ','LENT',1,5,None,None,'traditional option')
# TQ-2
add('GNM-TQ-2','meditabor','of','TQ','LENT',2,1,None,None,'2nd Sunday')
add('GNM-TQ-2','deus-in-adjutorium','in','TQ','LENT',2,5,None,None,'Thursday')
add('GNM-TQ-2','domine-ad-adjuvandum','of','TQ','LENT',2,5,None,None,'Thursday')
add('GNM-TQ-2','qui-manducat','co','TQ','LENT',2,5,None,None,'Thursday')
add('GNM-TQ-2','ego-autem-cum-justitia','in','TQ','LENT',2,6,None,None,'Friday')
# TQ-3
add('GNM-TQ-3','salus-populi','in','TQ','LENT',3,5,None,None,'Thursday')
add('GNM-TQ-3','si-ambulavero','of','TQ','LENT',3,5,None,None,'Thursday')
add('GNM-TQ-3','tu-mandasti','co','TQ','LENT',3,5,None,None,'Thursday')
# TQ-4
add('GNM-TQ-4','laetetur-cor','in','TQ','LENT',4,5,None,None,'Thursday')
add('GNM-TQ-4','precatus-est','of','TQ','LENT',4,5,None,None,'Thursday')
add('GNM-TQ-4','domine-memorabor','co','TQ','LENT',4,5,None,None,'Thursday')
# TQ-5
add('GNM-TQ-5','omnia-quae','in','TQ','LENT',5,5,None,None,'Thursday')
add('GNM-TQ-5','super-flumina','of','TQ','LENT',5,5,None,None,'Thursday')
add('GNM-TQ-5','memento-verbi','co','TQ','LENT',5,5,None,None,'Thursday')

# ===== EASTER =====
# TP-1 (Easter Octave Thu)
add('GNM-TP-1','victricem','in','PASC','OCT',1,5,None,None,'Thursday Easter Octave')
add('GNM-TP-1','in-die-solemnitatis','of','PASC','OCT',1,5,None,None,'Thursday Easter Octave')
add('GNM-TP-1','populus-acquisitionis','co','PASC','OCT',1,5,None,None,'Thursday Easter Octave')
# TP-2
add('GNM-TP-2','quasi-modo-geniti','in','PASC','AD_ASC',2,1,None,None,'Sunday (Divine Mercy)')
add('GNM-TP-2','deus-dum-egredereris','in','PASC','AD_ASC',2,5,None,None,'Thursday')
add('GNM-TP-2','redemisti-nos','in','PASC','AD_ASC',2,6,None,None,'Friday')
add('GNM-TP-2','accipite-iucunditatem','in','PASC','AD_ASC',2,None,None,None,'all other weekdays (Mon/Tue/Wed/Sat?)')
add('GNM-TP-2','angelus-domini','of','PASC','AD_ASC',2,None,None,None,'all days')
add('GNM-TP-2','mitte-manum-alleluia','co','PASC','AD_ASC',2,1,None,None,'Sunday')
add('GNM-TP-2','spiritus-ubi-vult','co','PASC','AD_ASC',2,2,None,None,'Monday')
add('GNM-TP-2','spiritus-ubi-vult','co','PASC','AD_ASC',2,3,None,None,'Tuesday')
# TP-3
add('GNM-TP-3','jubilate-deo','in','PASC','AD_ASC',3,None,None,None,'default in')
add('GNM-TP-3','repleatur-os','in','PASC','AD_ASC',3,4,None,None,'Wednesday')
add('GNM-TP-3','lauda-anima','of','PASC','AD_ASC',3,None,None,None,'all days')
add('GNM-TP-3','cantate-domino','co','PASC','AD_ASC',3,None,None,None,'default co')
add('GNM-TP-3','surrexit-dominus','co','PASC','AD_ASC',3,1,1,None,'Sunday A')
add('GNM-TP-3','simon-ioannis','co','PASC','AD_ASC',3,1,0,None,'Sunday C')
add('GNM-TP-3','video-caelos','co','PASC','AD_ASC',3,3,None,None,'Tuesday')
add('GNM-TP-3','panis-quem-ego','co','PASC','AD_ASC',3,5,None,None,'Thursday')
add('GNM-TP-3','qui-manducat','co','PASC','AD_ASC',3,6,None,None,'Friday')
# TP-4
add('GNM-TP-4','misericordia-domini','in','PASC','AD_ASC',4,None,None,None,'default in')
add('GNM-TP-4','deus-dum-egredereris','in','PASC','AD_ASC',4,5,None,None,'Thursday')
add('GNM-TP-4','redemisti-nos','in','PASC','AD_ASC',4,6,None,None,'Friday')
add('GNM-TP-4','deus-deus-meus','of','PASC','AD_ASC',4,None,None,None,'all days')
add('GNM-TP-4','ego-sum-pastor-bonus','co','PASC','AD_ASC',4,1,None,None,'Sunday')
add('GNM-TP-4','cantate-domino','co','PASC','AD_ASC',4,None,None,None,'weekdays')
add('GNM-TP-4','tanto-tempore','co','PASC','AD_ASC',4,7,None,None,'Saturday')

# ===== FEASTS =====
add('GNM-2-5','gaudeamus-agathae','in','','','','','',None,'FEAST: St. Agatha Feb 5')
add('GNM-2-5','afferentur-post-eam','of','','','','','',None,'FEAST: St. Agatha Feb 5')
add('GNM-2-5','feci-judicium','co','','','','','',None,'FEAST: St. Agatha Feb 5')

add('GNM-3-19','justus-ut-palma','in','','','','','',None,'FEAST: St. Joseph Mar 19')
add('GNM-3-19','veritas-mea','of','','','','','',None,'FEAST: St. Joseph Mar 19')
add('GNM-3-19','joseph-fili-david','co','','','','','',None,'FEAST: St. Joseph Mar 19')

add('GNM-6-11','mihi-autem-nimis','in','','','','','',None,'FEAST: St. Barnabas Jun 11')
add('GNM-6-11','constitues-eos','of','','','','','',None,'FEAST: St. Barnabas Jun 11')
add('GNM-6-11','vos-qui-secuti-estis-me','co','','','','','',None,'FEAST: St. Barnabas Jun 11')
add('GNM-6-11','vos-qui-secuti-estis-me-dicit-dominus','co','','','','','',None,'FEAST: St. Barnabas Jun 11 (or)')

add('GNM-7-3','mihi-autem-nimis','in','','','','','',None,'FEAST: St. Thomas Jul 3 — ant-only variant')
add('GNM-7-3','in-omnem-terram','of','','','','','',None,'FEAST: St. Thomas Jul 3')
add('GNM-7-3','mitte-manum','co','','','','','',None,'FEAST: St. Thomas Jul 3')

add('GNM-7-31','in-nomine-jesu','in','','','','','',None,'FEAST: St. Ignatius Jul 31')
add('GNM-7-31','veritas-mea','of','','','','','',None,'FEAST: St. Ignatius Jul 31')
add('GNM-7-31','qui-meditabitur','co','','','','','',None,'FEAST: St. Ignatius Jul 31')

add('GNM-Aug-14','venite-benedicti','in','','','','','',None,'FEAST: St. Maximilian Kolbe Aug 14 — ant variant')
add('GNM-Aug-14','deus-deus-meus','of','','','','','',None,'FEAST: St. Maximilian Kolbe Aug 14')
add('GNM-Aug-14','majorem-caritatem','co','','','','','',None,'FEAST: Aug 14 — file in Offertorium/ but annotated Co. II')

add('GNM-Aug-15','signum-magnum','in','','','','','',None,'FEAST: Assumption Aug 15')
add('GNM-Aug-15','gaudeamus-mariae-assumptione','in','','','','','',None,'FEAST: Assumption Aug 15 (or)')
add('GNM-Aug-15','assumpta-est-maria','of','','','','','',None,'FEAST: Assumption Aug 15')
add('GNM-Aug-15','beatam-me-dicent','co','','','','','',None,'FEAST: Assumption Aug 15 — english-f3.gabc')

add('GNM-Aug-21','statuit','in','','','','','',None,'FEAST: St. Pius X Aug 21')
add('GNM-Aug-21','benedicam-domino','of','','','','','',None,'FEAST: St. Pius X Aug 21 — english2 variant')
add('GNM-Aug-21','manducaverunt','co','','','','','',None,'FEAST: St. Pius X Aug 21')

add('GNM-Aug-28','in-medio-ecclesiae','in','','','','','',None,'FEAST: St. Augustine Aug 28')
add('GNM-Aug-28','justus-ut-palma','of','','','','','',None,'FEAST: St. Augustine Aug 28')
add('GNM-Aug-28','fidelis-servus','co','','','','','',None,'FEAST: St. Augustine Aug 28')

add('GNM-09-29','benedicite-dominum','in','','','','','',None,'FEAST: Archangels Sept 29')
add('GNM-09-29','stetit-angelus','of','','','','','',None,'FEAST: Archangels Sept 29')
add('GNM-09-29','benedicite-omnes-angeli','co','','','','','',None,'FEAST: Archangels Sept 29')
add('GNM-09-29','immittet-angelus','of','','','','','',None,'FEAST: Guardian Angels Oct 2')
add('GNM-09-29','in-conspectu-angelorum','co','','','','','',None,'FEAST: Guardian Angels Oct 2 — Missal option; file in Antiphona/')

csv_path = r'C:\Users\johna\Dropbox\Chant\GNM\gnm_assignments.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'source_file','slug','part','part_id','season','subseason','wknum','seq',
        'cycle_sun','cycle_wk','chant_group_id','status','notes'
    ])
    writer.writeheader()
    writer.writerows(rows)

resolved_ct = sum(1 for r in rows if r['status'] == 'RESOLVED')
needs_ct = sum(1 for r in rows if r['status'] == 'NEEDS_INPUT')
print(f'Wrote {len(rows)} rows to {csv_path}')
print(f'  RESOLVED: {resolved_ct}')
print(f'  NEEDS_INPUT: {needs_ct}')
