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
                del subrequests[-1]
                return subrequests[2:]

        elif subrequests[0] == "2":
            if subrequests[1] == "1":
                return True
            return False

        elif subrequests[0] == "3":
            if subrequests[1] == "1":
                return True
            return False

        elif subrequests[0] == "4":
            if subrequests[1] == "-1":
                return False

        elif subrequests[0] == '5':
            if subrequests[1] == "-1":
                return False
            return subrequests[1]

        elif subrequests[0] == '6':
            if subrequests[1] == "0":
                return False
            if subrequests[1] == "-1":
                return 'wait'
            return subrequests[1]

        elif subrequests[0] == "7":
            if subrequests[1] == "0":
                return False
            return subrequests[1]

        elif subrequests[0] == "8":
            if subrequests[1] == "1":
                return True
            return False
