"""
Static class
Parse the incoming message from the server and return the appropriate value
"""

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

        elif subrequests[0] == '4':
            if subrequests[1] == '-1':
                return False
            elif subrequests[1] == '0':
                if len(subrequests) == 3:
                    return "0", [], subrequests[2]
                return "0", [], []
            elif subrequests[1] == '1':
                if len(subrequests) == 4:
                    return "1", subrequests[2], subrequests[3]
                return "1", subrequests[2], []
            elif subrequests[1] == '2':
                return subrequests[2:]
            elif subrequests[1] == '4':
                if len(subrequests) == 4:
                    return "4", subrequests[2], subrequests[3]
                return "4", subrequests[2], []

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

        elif subrequests[0] == '10':
            if subrequests[1] == "0":
                return False
            return True

        elif subrequests[0] == '9':
            if subrequests[1] == "0":
                return False
            if subrequests[1] == '-1':
                return 1
            else:
                print subrequests, 'subrequests'
                if len(subrequests) == 4:
                    return subrequests[1], subrequests[2], subrequests[3]
                if len(subrequests) == 3:
                    return subrequests[1], subrequests[2], []
                return subrequests[1], []

        elif subrequests[0] == "7":
            if subrequests[1] == "0":
                return False
            return subrequests[1]

        elif subrequests[0] == "8":
            if subrequests[1] == "1":
                return True
            return False

        elif subrequests[0] == '11':
            if subrequests[1] == '-1':
                return False
            elif subrequests[1] == '0':
                return "0"
            elif subrequests[1] == '1':
                return "restart"
            elif subrequests[1] == '2':
                return "kill"


        elif subrequests[0] == '12':
            if subrequests[1] == '-1':
                return False
            else:
                print subrequests, 'sub 12'
                return subrequests[1]