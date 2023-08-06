from ovotestkit.func import OMTClient


def test_get_entry():
    omt = OMTClient('whatever','whatever')
    entry = omt.get_entry(target_tbl='ovo_gold.ovo_spring_activity_report')
    print(entry.source_kpi, entry.target_kpi)


if __name__ == "__main__":
    test_get_entry()