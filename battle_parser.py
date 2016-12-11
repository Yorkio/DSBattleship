class Parser:
    @staticmethod
    def parse(request):
        subrequests = request.split("#")

        if len(subrequests) == 0:
            return 0

        if subrequests[0] == "0":
            if subrequests[1] == "1":
                return True
            return False

        if subrequests[0] == "1":
            return subrequests
