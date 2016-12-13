class Parser:
    @staticmethod
    def parse(request):
        subrequests = request.split("#")

        if len(subrequests) == 0:
            return 0

        elif subrequests[0] == "0":
            if subrequests[1] == "1":
                return True
            return False

        elif subrequests[0] == "1":
            if subrequests[1] == "0":
                return False
            else:
                return subrequests[4:]

        elif subrequests[0] == "2":
            if subrequests[1] == "1":
                return True
            return False

        elif subrequests[0] == "3":
            if subrequests[1] == "1":
                return True
            return False

