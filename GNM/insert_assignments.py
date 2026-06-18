"""Insert lit_part_assignment records for GNM chants (OT, Lent, Feasts).
Easter weeks skipped (already have assignments)."""

import keyring
from sqlalchemy import create_engine, text

pw_rw = keyring.get_password('liturgio-mysql', 'jcost')
engine = create_engine(f'mysql+mysqlconnector://jcost:{pw_rw}@localhost:3306/liturgio')

PART = {'in': 1, 'of': 8, 'co': 9}

CG = {
    'in-excelso-throno': 20, 'dominus-secus-mare': 693, 'venite-adoremus': 450,
    'dominus-fortitudo': 522, 'dum-clamarem': 299, 'ego-autem-cum-justitia': 830,
    'deus-in-loco-sancto': 1026, 'sitientes': 776, 'justus-es': 1284,
    'in-voluntate': 1047, 'si-iniquitates': 8690, 'ne-derelinquas': 7759,
    'dicit-dominus-ego': 3923, 'loquetur-dominus': 271, 'invocabit-me': 327,
    'mihi-autem-nimis': 5848, 'in-nomine-jesu': 18080, 'statuit': 456,
    'jubilate-deo-universa': 937, 'perfice-gressus': 265,
    'benedicam-domino': 11077, 'populum-humilem': 1080,
    'precatus-est': 325, 'in-te-speravi': 967, 'exspectans-exspectavi': 13717,
    'oravi-deum': 652, 'vir-erat': 1363, 'meditabor': 810,
    'domine-vivifica': 109, 'domine-ad-adjuvandum': 731, 'super-flumina': 812,
    'notas-mihi': 6934, 'laetabimur': 1296, 'dicit-andreas': 1021,
    'multitudo-languentium': 1267, 'comedite-pinguia': 496,
    'quicumque-fecerit': 957, 'unam-petii': 574, 'quod-dico-vobis': 1002,
    'passer-invenit': 1090, 'ecce-sto': 164, 'simile-est': 6271,
    'petite': 5618, 'panem-de-caelo': 388, 'beatus-servus': 1154,
    'domine-memorabor': 1318, 'dico-vobis': 1058, 'hoc-corpus': 726,
    'in-salutari': 1290, 'dico-autem-vobis': 699, 'fidelis-servus': 3902,
    'amen-dico-vobis-quidquid': 592, 'jerusalem-quae-aedificatur': 13460,
    'memento-verbi': 696, 'feci-judicium': 844, 'qui-meditabitur': 582,
    'manducaverunt': 677, 'benedicite-omnes-angeli': 1127,
    'omnis-terra': 13, 'adorate-deum': 1123, 'laetetur-cor': 864,
    'suscepimus': 1781, 'ecce-deus': 1357, 'exsultate-deo': 1323,
    'deus-in-adjutorium': 501, 'inclina-domine': 1165, 'da-pacem': 172,
    'salus-populi': 389, 'ego-clamavi': 558, 'misereris-omnium': 533,
    'intret-oratio': 238, 'verba-mea': 1248, 'omnia-quae': 1056,
    'venite-benedicti': 997, 'signum-magnum': 23, 'in-medio-ecclesiae': 233,
    'benedicite-dominum': 985, 'jubilate-deo-omnis': 718,
    'dextera-domini': 47, 'bonum-est-confiteri': 1194,
    'ad-te-domine': 962, 'justitiae-domini': 591, 'exaltabo-te': 648,
    'sanctificavit': 838, 'domine-in-auxilium': 993, 'si-ambulavero': 616,
    'recordare-mei': 67, 'benedic-anima-mea': 1359, 'gressus-meos': 1099,
    'deus-deus-meus': 924, 'veritas-mea': 630, 'constitues-eos': 1319,
    'in-omnem-terram': 3360, 'majorem-caritatem': 401, 'immittet-angelus': 747,
    'venite-post-me': 552, 'ego-vos-elegi': 470, 'mirabantur': 1148,
    'illumina-faciem': 640, 'beati-mundo-corde': 345, 'introibo': 554,
    'mense-septimo': 1149, 'circuibo': 1079, 'qui-vult-venire': 89,
    'gustate': 1203, 'qui-manducat': 798, 'acceptabis': 1221,
    'optimam-partem': 3316, 'honora-dominum': 1145, 'panis-quem': 782,
    'de-fructu': 1245, 'domine-quinque-talenta': 383, 'vovete': 1134,
    'tollite-hostias': 404, 'tu-mandasti': 479, 'beata-viscera': 160,
    'aufer-a-me': 828, 'domine-dominus-noster': 998, 'dominus-regit-me': 278,
    'quinque-prudentes': 3388, 'domus-mea': 43, 'laudate-dominum': 322,
    'tanto-tempore': 13575, 'joseph-fili-david': 139, 'mitte-manum': 589,
    'beatam-me-dicent': 286, 'de-profundis': 986, 'respice-domine': 691,
    'assumpta-est-maria': 3317,
    'miserere-mihi-ad-te': 335, 'gaudeamus-agathae': 1183,
    'gaudeamus-mariae-assumptione': 3312, 'vos-qui-secuti-estis-me': 1028,
    'vos-qui-secuti-estis-me-dicit-dominus': 97, 'afferentur-post-eam': 768,
    'justus-ut-palma-in': 3816, 'justus-ut-palma-of': 3841,
    # Resolved from user's local_chants fixes
    'exaudi-domine': 396, 'stetit-angelus': 302,
    'ego-sum-pastor-bonus': 95, 'in-conspectu-angelorum': 3302,
    # Approximate (needs_review will catch)
    'laetatur-cor': 864,  # likely same as laetetur-cor
    'quinque-prudentes-virgines': 3388,
    'de-ventre-matris-meae': 659,
}

SKIP = {'dicit-dominus-implete-hydrias'}

assignments = []

def add(slug, part, epoch_slug, cycle_sun=None, cycle_wk=None,
        authority='GRADUALE', notes=None):
    if slug in SKIP:
        return
    if slug == 'justus-ut-palma':
        key = f'justus-ut-palma-{"in" if part == "in" else "of"}'
    else:
        key = slug
    cg_id = CG.get(key)
    if cg_id is None:
        print(f'  SKIP (no cg_id): {slug} ({part}) at {epoch_slug}')
        return
    assignments.append({
        'jurisdiction': 'UNIVERSAL',
        'part_id': PART[part],
        'lit_epoch_slug': epoch_slug,
        'cycle_sun': cycle_sun,
        'cycle_wk': cycle_wk,
        'chant_group_id': cg_id,
        'assignment_authority_code': authority,
        'notes': notes,
    })

# ===== ORDINARY TIME =====
# Slug format: OT-OT-{wk:02d} (week) or OT-OT-{wk:02d}-{seq} (day)

add('in-excelso-throno','in','OT-OT-01')
add('jubilate-deo-omnis','of','OT-OT-01')
add('notas-mihi','co','OT-OT-01')
add('venite-post-me','co','OT-OT-01-2', notes='Mon if Baptism not celebrated on Sun')

add('omnis-terra','in','OT-OT-02')
add('jubilate-deo-universa','of','OT-OT-02')
add('laetabimur','co','OT-OT-02')
add('dicit-andreas','co','OT-OT-02-1', cycle_sun=2)
add('dicit-dominus-implete-hydrias','co','OT-OT-02-1', cycle_sun=0)
add('multitudo-languentium','co','OT-OT-02-5')
add('ego-vos-elegi','co','OT-OT-02-6')

add('adorate-deum','in','OT-OT-03')
add('dominus-secus-mare','in','OT-OT-03-1', cycle_sun=1)
add('dominus-secus-mare','in','OT-OT-03-1', cycle_sun=2)
add('dextera-domini','of','OT-OT-03')
add('mirabantur','co','OT-OT-03')
add('venite-post-me','co','OT-OT-03-1', cycle_sun=1)
add('venite-post-me','co','OT-OT-03-1', cycle_sun=2)
add('comedite-pinguia','co','OT-OT-03-1', cycle_sun=0)
add('quicumque-fecerit','co','OT-OT-03-3')

add('laetetur-cor','in','OT-OT-04')
add('bonum-est-confiteri','of','OT-OT-04')
add('illumina-faciem','co','OT-OT-04')
add('beati-mundo-corde','co','OT-OT-04-1', cycle_sun=1)

add('venite-adoremus','in','OT-OT-05')
add('perfice-gressus','of','OT-OT-05')
add('introibo','co','OT-OT-05')
add('multitudo-languentium','co','OT-OT-05-1', cycle_sun=2)
add('multitudo-languentium','co','OT-OT-05-2', cycle_wk=1)
add('mense-septimo','co','OT-OT-05-2', cycle_wk=0)

add('exaudi-domine','in','OT-OT-11')
add('benedicam-domino','of','OT-OT-11')
add('unam-petii','co','OT-OT-11')

add('dominus-fortitudo','in','OT-OT-12')
add('perfice-gressus','of','OT-OT-12')
add('circuibo','co','OT-OT-12')
add('quod-dico-vobis','co','OT-OT-12-1', cycle_sun=1)
add('qui-vult-venire','co','OT-OT-12-1', cycle_sun=0)

add('suscepimus','in','OT-OT-14')
add('populum-humilem','of','OT-OT-14')
add('gustate','co','OT-OT-14')

add('dum-clamarem','in','OT-OT-15')
add('ego-autem-cum-justitia','in','OT-OT-15', notes='or (option 2)')
add('ad-te-domine','of','OT-OT-15')
add('qui-manducat','co','OT-OT-15')
add('passer-invenit','co','OT-OT-15', notes='or')

add('ecce-deus','in','OT-OT-16')
add('justitiae-domini','of','OT-OT-16')
add('acceptabis','co','OT-OT-16')
add('optimam-partem','co','OT-OT-16-1', cycle_sun=0)
add('ecce-sto','co','OT-OT-16', notes='additional option')

add('deus-in-loco-sancto','in','OT-OT-17')
add('exsultate-deo','in','OT-OT-17-6', cycle_wk=1)
add('exaltabo-te','of','OT-OT-17')
add('honora-dominum','co','OT-OT-17')
add('simile-est','co','OT-OT-17-1', cycle_sun=1)
add('petite','co','OT-OT-17-1', cycle_sun=0)

add('deus-in-adjutorium','in','OT-OT-18')
add('sitientes','in','OT-OT-18-1', cycle_sun=1)
add('precatus-est','of','OT-OT-18')
add('sanctificavit','of','OT-OT-18-1', cycle_sun=0)
add('panem-de-caelo','co','OT-OT-18')
add('qui-vult-venire','co','OT-OT-18-6')

add('respice-domine','in','OT-OT-19')
add('in-te-speravi','of','OT-OT-19')
add('panis-quem','co','OT-OT-19')
add('beatus-servus','co','OT-OT-19', notes='or')

add('inclina-domine','in','OT-OT-21')
add('exspectans-exspectavi','of','OT-OT-21')
add('de-fructu','co','OT-OT-21')
add('qui-manducat','co','OT-OT-21', notes='or')
add('beatus-servus','co','OT-OT-21-5')
add('quinque-prudentes-virgines','co','OT-OT-21-6')
add('domine-quinque-talenta','co','OT-OT-21-7')

add('miserere-mihi-ad-te','in','OT-OT-22')
add('domine-in-auxilium','of','OT-OT-22')
add('domine-memorabor','co','OT-OT-22')
add('qui-vult-venire','co','OT-OT-22-1', cycle_sun=1)
add('mirabantur','co','OT-OT-22-2')
add('multitudo-languentium','co','OT-OT-22-4')

add('justus-es','in','OT-OT-23')
add('oravi-deum','of','OT-OT-23')
add('vovete','co','OT-OT-23')
add('multitudo-languentium','co','OT-OT-23-3')

add('da-pacem','in','OT-OT-24')
add('sanctificavit','of','OT-OT-24')
add('precatus-est','of','OT-OT-24-1', cycle_sun=0)
add('tollite-hostias','co','OT-OT-24')
add('qui-vult-venire','co','OT-OT-24-1', cycle_sun=2)
add('dico-vobis','co','OT-OT-24-1', cycle_sun=0)
add('hoc-corpus','co','OT-OT-24-2', cycle_wk=0)

add('salus-populi','in','OT-OT-25')
add('si-ambulavero','of','OT-OT-25')
add('tu-mandasti','co','OT-OT-25')

add('dum-clamarem','in','OT-OT-26')
add('ego-autem-cum-justitia','in','OT-OT-26', notes='or (option 2)')
add('ad-te-domine','of','OT-OT-26')
add('qui-manducat','co','OT-OT-26')
add('passer-invenit','co','OT-OT-26', notes='or')

add('in-voluntate','in','OT-OT-27')
add('de-ventre-matris-meae','in','OT-OT-27-3', cycle_wk=0, notes='ad libitum')
add('vir-erat','of','OT-OT-27')
add('in-salutari','co','OT-OT-27')
add('optimam-partem','co','OT-OT-27-3')
add('petite','co','OT-OT-27-5')
add('beata-viscera','co','OT-OT-27-7')

add('si-iniquitates','in','OT-OT-28')
add('recordare-mei','of','OT-OT-28')
add('aufer-a-me','co','OT-OT-28')
add('dico-autem-vobis','co','OT-OT-28', notes='or')

add('ego-clamavi','in','OT-OT-29')
add('meditabor','of','OT-OT-29')
add('domine-dominus-noster','co','OT-OT-29')
add('beatus-servus','co','OT-OT-29-3')
add('fidelis-servus','co','OT-OT-29-4')

add('laetatur-cor','in','OT-OT-30', notes='slug laetatur-cor; verify = laetetur-cor cg 864')
add('domine-vivifica','of','OT-OT-30')
add('laetabimur','co','OT-OT-30')

add('ne-derelinquas','in','OT-OT-31')
add('misereris-omnium','in','OT-OT-31-1', cycle_sun=0)
add('benedic-anima-mea','of','OT-OT-31')
add('notas-mihi','co','OT-OT-31')
add('dico-vobis','co','OT-OT-31-5', notes='optional')

add('intret-oratio','in','OT-OT-32')
add('gressus-meos','of','OT-OT-32')
add('dominus-regit-me','co','OT-OT-32')
add('quinque-prudentes','co','OT-OT-32-1', cycle_sun=1)

add('dicit-dominus-ego','in','OT-OT-33')
add('de-profundis','of','OT-OT-33')
add('amen-dico-vobis-quidquid','co','OT-OT-33')
add('domine-quinque-talenta','co','OT-OT-33-1', cycle_sun=1)
add('domine-quinque-talenta','co','OT-OT-33-4')
add('domus-mea','co','OT-OT-33-6')

add('loquetur-dominus','in','OT-OT-34', notes='weekdays only; Sun=Christ the King')
add('bonum-est-confiteri','of','OT-OT-34', notes='weekdays only')
add('jerusalem-quae-aedificatur','co','OT-OT-34')
add('laudate-dominum','co','OT-OT-34', notes='or')

# ===== LENT =====
# Slug format: TQ-LENT-{wk:02d}-{seq}

# Ash Wed week — Thu = seq 5, wk 0
add('dum-clamarem','in','TQ-LENT-00-5')
add('ad-te-domine','of','TQ-LENT-00-5')
add('qui-vult-venire','co','TQ-LENT-00-5')
add('acceptabis','co','TQ-LENT-00-5', notes='traditional option')

add('invocabit-me','in','TQ-LENT-01-1')
add('verba-mea','in','TQ-LENT-01-5')
add('recordare-mei','of','TQ-LENT-01-5')
add('petite','co','TQ-LENT-01-5')
add('acceptabis','co','TQ-LENT-01-5', notes='traditional option')

add('meditabor','of','TQ-LENT-02-1')
add('deus-in-adjutorium','in','TQ-LENT-02-5')
add('domine-ad-adjuvandum','of','TQ-LENT-02-5')
add('qui-manducat','co','TQ-LENT-02-5')
add('ego-autem-cum-justitia','in','TQ-LENT-02-6')

add('salus-populi','in','TQ-LENT-03-5')
add('si-ambulavero','of','TQ-LENT-03-5')
add('tu-mandasti','co','TQ-LENT-03-5')

add('laetetur-cor','in','TQ-LENT-04-5')
add('precatus-est','of','TQ-LENT-04-5')
add('domine-memorabor','co','TQ-LENT-04-5')

add('omnia-quae','in','TQ-LENT-05-5')
add('super-flumina','of','TQ-LENT-05-5')
add('memento-verbi','co','TQ-LENT-05-5')

# ===== FEASTS =====

add('gaudeamus-agathae','in','st-agatha')
add('afferentur-post-eam','of','st-agatha')
add('feci-judicium','co','st-agatha')

add('justus-ut-palma','in','st-joseph')
add('veritas-mea','of','st-joseph')
add('joseph-fili-david','co','st-joseph')

add('mihi-autem-nimis','in','st-barnabas')
add('constitues-eos','of','st-barnabas')
add('vos-qui-secuti-estis-me','co','st-barnabas')
add('vos-qui-secuti-estis-me-dicit-dominus','co','st-barnabas', notes='or')

add('mihi-autem-nimis','in','st-thomas-apostle', notes='antiphon-only variant')
add('in-omnem-terram','of','st-thomas-apostle')
add('mitte-manum','co','st-thomas-apostle')

add('in-nomine-jesu','in','st-ignatius-loyola')
add('veritas-mea','of','st-ignatius-loyola')
add('qui-meditabitur','co','st-ignatius-loyola')

add('venite-benedicti','in','st-maximilian-kolbe', notes='antiphon variant')
add('deus-deus-meus','of','st-maximilian-kolbe')
add('majorem-caritatem','co','st-maximilian-kolbe',
    authority='MISSAL', notes='Offertory chant used as Communion per Missal text match')

add('signum-magnum','in','assumption')
add('gaudeamus-mariae-assumptione','in','assumption', notes='or')
add('assumpta-est-maria','of','assumption')
add('beatam-me-dicent','co','assumption', notes='english-f3.gabc variant')

add('statuit','in','st-pius-x')
add('benedicam-domino','of','st-pius-x', notes='english2 variant')
add('manducaverunt','co','st-pius-x')

add('in-medio-ecclesiae','in','st-augustine')
add('justus-ut-palma','of','st-augustine')
add('fidelis-servus','co','st-augustine')

add('benedicite-dominum','in','archangels')
add('stetit-angelus','of','archangels')
add('benedicite-omnes-angeli','co','archangels')

add('immittet-angelus','of','guardian-angels')
add('in-conspectu-angelorum','co','guardian-angels',
    authority='MISSAL', notes='Antiphon used as Communion per Missal')

# ===== EXECUTE =====

new_saints_pos = [
    ('UNIVERSAL','st-agatha','Saint Agatha, Virgin and Martyr','MEMORIAL',2,5),
    ('UNIVERSAL','st-barnabas','Saint Barnabas, Apostle','MEMORIAL',6,11),
    ('UNIVERSAL','st-thomas-apostle','Saint Thomas, Apostle','FEAST',7,3),
    ('UNIVERSAL','st-ignatius-loyola','Saint Ignatius of Loyola, Priest','MEMORIAL',7,31),
    ('UNIVERSAL','st-maximilian-kolbe','Saint Maximilian Kolbe, Priest and Martyr','MEMORIAL',8,14),
    ('UNIVERSAL','st-pius-x','Saint Pius X, Pope','MEMORIAL',8,21),
    ('UNIVERSAL','st-augustine','Saint Augustine, Bishop and Doctor of the Church','MEMORIAL',8,28),
    ('UNIVERSAL','archangels','Saints Michael, Gabriel, and Raphael, Archangels','FEAST',9,29),
    ('UNIVERSAL','guardian-angels','The Holy Guardian Angels','MEMORIAL',10,2),
]

new_epochs = [
    ('st-agatha','saint','Saint Agatha, Virgin and Martyr'),
    ('st-barnabas','saint','Saint Barnabas, Apostle'),
    ('st-thomas-apostle','saint','Saint Thomas, Apostle'),
    ('st-ignatius-loyola','saint','Saint Ignatius of Loyola, Priest'),
    ('st-maximilian-kolbe','saint','Saint Maximilian Kolbe, Priest and Martyr'),
    ('st-pius-x','saint','Saint Pius X, Pope'),
    ('st-augustine','saint','Saint Augustine, Bishop and Doctor of the Church'),
    ('archangels','saint','Saints Michael, Gabriel, and Raphael, Archangels'),
    ('guardian-angels','saint','The Holy Guardian Angels'),
]

with engine.begin() as conn:
    # Create missing proper_of_saints entries
    for j, slug, name, rank, m, d in new_saints_pos:
        existing = conn.execute(text(
            'SELECT 1 FROM proper_of_saints WHERE jurisdiction=:j AND slug=:s'
        ), {'j': j, 's': slug}).fetchone()
        if existing:
            print(f'  proper_of_saints {slug} already exists')
        else:
            conn.execute(text('''
                INSERT INTO proper_of_saints
                (jurisdiction, slug, common_name, rank_code, month_nominal, day_nominal)
                VALUES (:j, :s, :n, :r, :m, :d)
            '''), {'j': j, 's': slug, 'n': name, 'r': rank, 'm': m, 'd': d})
            print(f'  Created proper_of_saints: {slug}')

    # Create missing lit_epoch entries for saints
    for slug, kind, title in new_epochs:
        existing = conn.execute(text(
            'SELECT 1 FROM lit_epoch WHERE slug=:s'
        ), {'s': slug}).fetchone()
        if existing:
            print(f'  lit_epoch {slug} already exists')
        else:
            conn.execute(text('''
                INSERT INTO lit_epoch (slug, kind, title)
                VALUES (:s, :k, :t)
            '''), {'s': slug, 'k': kind, 't': title})
            print(f'  Created lit_epoch: {slug}')

    # Insert assignments
    inserted = 0
    for a in assignments:
        conn.execute(text('''
            INSERT INTO lit_part_assignment
            (jurisdiction, part_id, lit_epoch_slug, cycle_sun, cycle_wk,
             chant_group_id, assignment_authority_code, notes, needs_review)
            VALUES (:jurisdiction, :part_id, :lit_epoch_slug, :cycle_sun, :cycle_wk,
                    :chant_group_id, :assignment_authority_code, :notes, 1)
        '''), a)
        inserted += 1

    print(f'\nInserted {inserted} lit_part_assignment records (all needs_review=1)')
    print(f'Skipped: {SKIP}')
