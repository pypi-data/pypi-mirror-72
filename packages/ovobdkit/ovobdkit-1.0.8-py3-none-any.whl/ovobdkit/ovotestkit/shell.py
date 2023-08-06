from bash import bash
class ImpalaShell:
    @classmethod
    def execute(cls, Q):
        b = bash(f"impala-shell -i bddevdn0001.bigdata.ovo.id -d default -k -q '{Q}'")
        out = b.stdout
        return out.decode('utf-8')

