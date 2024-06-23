
class ResultValueUnifier:
    def __init__(self):
        self._result_number:int = 0
        self._correct_rate_sum:float = 0
        self._redundant_rate_sum:float = 0
        self._redundant_number:int = 0
        self._lack_rate_sum:float = 0
        self._lack_number:int = 0
    #-------------------------------------------------------------------
    def get_dict_data(self)->dict[str, float]:
        from .. import info_key
        return{
            info_key.AVG_CORRECT_RATE_KEY:self.get_avg_correct_rate(),
            info_key.AVG_REDUNDANT_RATE_KEY:self.get_avg_redundant_rate(),
            info_key.AVG_LACK_RATE_KEY:self.get_avg_lack_rate(),
        }
    #-------------------------------------------------------------------
    def add_result(self, result):
        from . import process_result
        result:process_result.ProcessResult = result
        self._result_number += 1
        self._correct_rate_sum += result.get_correct_rate()
        redundant_rate = result.get_redundant_rate()
        if( redundant_rate!=None ):
            self._redundant_rate_sum += redundant_rate
            self._redundant_number += 1
        lack_rate = result.get_lack_rate()
        if( lack_rate!=None ):
            self._lack_rate_sum += lack_rate
            self._lack_number += 1
    #--------------------------------------------------------------------
    def get_avg_correct_rate(self)->float:
        return self._correct_rate_sum / self._result_number
    #--------------------------------------------------------------------
    def get_avg_redundant_rate(self)->float:
        if( self._redundant_number <= 0 ):return None
        return self._redundant_rate_sum / self._redundant_number
    #--------------------------------------------------------------------
    def get_avg_lack_rate(self)->float:
        if( self._lack_number <= 0 ):return None
        return self._lack_rate_sum / self._lack_number
#========================================================================