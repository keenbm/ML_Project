import os 
import sys

class HousingException(Exception):

    def __init__(self,error_message:Exception,error_detail:sys):
        ## error_message:Exception-->Creats object when Excption occurs
        ## error_detail:sys--> Gives which line is causing error

        super().__init__(error_message) ## Inhereting from original Exception
        self.error_message=HousingException.get_detailed_error_message(error_message=error_message,
                                                                       error_detail=error_detail)
    
   
    @staticmethod ## We can directly call this method without creating object
    def get_detailed_error_message(error_message:Exception,error_detail:sys)->str:
        # ->str : Means function return string type data
        
        
        _,_ , exec_tb=error_detail.exc_info() ## return most recent exception
        
        line_number=exec_tb.tb_frame.f_lineno ## Get error line number
        file_name=exec_tb.tb_frame.f_code.co_filename ## Get error file name

        error_message=f"Error occured in scrip:[{file_name}] at line number : [{line_number}] error message:[{error_message}]"

        return error_message

    def __str__(self):
        return self.error_message


    def __repr__(self) -> str:
        return HousingException.__name__.str()