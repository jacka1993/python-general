import re
import logging

LOGGER = logging.getLogger(__name__)

################## Data parse functions
def cleanString(inputString, stringType="alphanumeric"):

    if stringType == "alphanumeric":
        regex = re.compile(r'\W+')
        outputString = regex.sub('', inputString)

    elif stringType == "alphanumericSpace":
        regex = re.compile(r'([^\s\w]|_)+')
        outputString = regex.sub('', inputString)

    elif stringType == "numeric":
        outputString = re.sub('[^0-9]', '', inputString)

    elif stringType == "numericPeriod":
        currencyFormat = re.compile(r'^(?!0\.00)\d{1,3}(,\d{3})*(\.\d\d)?$')
        result = currencyFormat.match(inputString)
        regex = re.compile(r'[^\d.]+')

        if result == None:
            # numbers like $13,70
            inputString = inputString.replace(",", ".")

        outputString = regex.sub('', inputString)
        if outputString.count(".") > 1:
            outputString = outputString.replace(".", "",
                                                outputString.count(".") - 1)
    else:
        outputString = inputString

    return outputString

#Y/N columns relate to gross amount:
#< $82.50
#> $82.50 but <$1,000
#> $1,000
class Validation:
  def __init__(self):
    self.isTaxInvoice= ["N", "N", "Y"]
    self.vendorName = ["N", "Y", "Y"]
    self.vendorABN = ["Y", "Y", "Y"]
    self.address = ["N", "N", "Y"]
    self.recipientABN = ["N", "N", "N"]  #NNY
    self.date = ["Y", "Y", "Y"]
    self.description = ["N", "Y", "Y"]
    self.quantity = ["N", "N", "N"]  #NYY
    self.totalAmount = ["Y", "Y", "Y"]
    self.gstAmount = ["N", "Y", "Y"]
    self.gstInclusive = ["N", "N", "N"]
    self.netAmount = ["N", "N", "N"]

  def validate_classification(self, textblock, state):
    validity = "VALID"
    reason = ""
    try:
        for attr, value in self.__dict__.items():
            if value[state] == "Y":
                if attr in textblock:
                    blockValue = textblock[attr]
                    if blockValue == "":
                        validity = "INVALID"
                        reason = reason + attr + ','
                else:
                    validity = "INVALID"
                    reason = reason + attr + ','

        return reason

    #error if no classification found
    except:
        print("----- Error on validate_classification -----")
        return "INVALID"

def validate_text_blocks(classifications):
    validationState = 0
    validationCheck = Validation()
    textblock = {}
    reason = ""

    # Convert classifications from textblocks to string
    for key, value in classifications.items():
        words = [x['text'] for x in value]
        if len(words) >= 1:
            textblock[key] = words[0]
        else:
            textblock[key] = ''

    totalAmount = textblock['totalAmount']
    
    # try to process total amount, else classify as invalid
    try:
        totalAmount = cleanString(totalAmount, stringType="numericPeriod")
            
        totalAmount = float(totalAmount)
        
        if totalAmount < 82.50:
            validationState = 0
        elif totalAmount > 1000:
            validationState = 2
        else:
            validationState = 1

        reason = validationCheck.validate_classification(textblock, validationState)

    except:
        print("----- Invalid totalAmount field -----")
        reason = "totalAmount"
        
    return reason

def validate_classifications(msg):
    LOGGER.info('Starting to validate textBlocks data')
    if isinstance(msg,dict):
        reason = validate_text_blocks(msg['classifications'])

    if reason == "":
        return { "validity": "VALID" }
    else:
        return { "validity": "INVALID", "reason": reason }
