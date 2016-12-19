#!/usr/bin/python3.5

# import requests
# requests does NOT how to deal with local file
# page = requests.get('/home/AttBilling/AT&T.html')
import sys
from lxml import html

# Read Name List from file and Determine accountSize
# Match number with names
if len(sys.argv) == 2:
    with open(sys.argv[1]) as f:
        names = list(filter(lambda x: len(x) != 0, [i.strip() for i in f.readlines()]))
        accountSize = len(names)

        numberNames = {}
        for i in names:
            numberNames[i[:i.find(':')]] = i[i.find(':') + 1:]
        # print(numberNames)
else:
    print('The number of Arguments in WRONG!')
    sys.exit(0)
# Python3 placeholder: {}, use format() to fill
print('Account Size:\t{}\n'.format(accountSize))

# Open HTML files and parse them
# with open(r'/home/chen/AttBilling/Jan20-Feb19/AT&T.html', "r") as f:
# with open(r'/home/chen/AttBilling/Jun20-Jul19/AT&T.html', "r") as f:
with open(r'/home/chen/AttBilling/Jul20-Aug19/AT&T.html', "r") as f:
# with open(r'/home/chen/AttBilling/Aug20-Sept19/AT&T.html', "r") as f:
# with open(r'/home/chen/AttBilling/Sept20-Oct19/AT&T.html', "r") as f:
# with open(r'/home/chen/AttBilling/Oct20-Nov19/Billing & Usage - AT&T.html', "r") as f:
    page = f.read()
tree = html.fromstring(page)
info = tree.xpath('//div[contains(@class, "accSummary")]//div[contains(@class, "accRow")]//text()')
cycleDateInfo = tree.xpath('//h3//text()')
# print(cycleDate)
# print(info)

# with open(r'/home/chen/AttBilling/Jan20-Feb19/data/Billing & Usage - AT&T.html', "r") as f:
# with open(r'/home/chen/AttBilling/Jun20-Jul19/data/Billing & Usage - AT&T.html', "r") as f:
with open(r'/home/chen/AttBilling/Jul20-Aug19/data/Billing & Usage - AT&T.html', "r") as f:
# with open(r'/home/chen/AttBilling/Aug20-Sept19/data/Billing & Usage - AT&T.html', "r") as f:
# with open(r'/home/chen/AttBilling/Sept20-Oct19/data/Billing & Usage - AT&T.html', "r") as f:
# with open(r'/home/chen/AttBilling/Oct20-Nov19/data/Billing & Usage - AT&T.html', "r") as f:
    page = f.read()
tree = html.fromstring(page)
numInfo = tree.xpath('//td[@headers="member_head"]//span//text()')
# print(numInfo)
dataInfo = tree.xpath('//a[@title="Web Usage"]//text()')
# print(dataInfo)
cycleDateInfoFromData = [i.strip() for i in tree.xpath('//div[@id="timeRange"]//text()')]
# print(cycleDateInfoFromData)

# \t\n\r trimming for unicode results
# The following are for string representation(unencoded)
# python2: unicode = python3: str
# The following are for raw byte representation
# python2: str = python3: bytes
# http://stackoverflow.com/questions/18034272/python-str-vs-unicode-types

# before strip(): <class 'lxml.etree._ElementUnicodeResult'>
# after strip(): <class 'str'>

# Try to use lambda/map/list to rewrite the following for loop!
# trimmedInfo = map(str.strip('\t\n\r'), info)

# Since the Unicode strings are unencoded. PLEASE encode it
# with ASCII with the help of ord() and chr()!!
# This will help with the comparison tremendously!
# Work Around: just use Unicode character chr(8722) for now

# The following list(map(...)) are equivalent to list comprehension!
# info = list(map(lambda x: x.strip(), info))
# numInfo = list(map(lambda x: x.strip(), numInfo))
# dataInfo = list(map(lambda x: x.strip(), dataInfo))
info = [i.strip() for i in info]
cycleDateInfo = [i.strip() for i in cycleDateInfo]
numInfo = [i.strip() for i in numInfo]
dataInfo = [i.strip() for i in dataInfo]

# Get date for this cycle from Info Sheet
cycleDate = ''
for i in cycleDateInfo:
    if i[:15] == 'New charges for':
        cycleDate = i[16:]

# Get date for this cycle from Data Sheet
cycleDateFromData = cycleDateInfoFromData[0]

# Get Total Data Used and Individual Data Usage
numInfo = [i.replace('.', '') for i in numInfo]
individualData = [None] * accountSize
count = 0
circularCount = 0
totalData = 0

# How Python Iterator works:
# Think of for loop as a function that
# takes an itr object as an argument.
# Each time it OUTPUTs the next() status
# of the itr object and update the internal
# counters in the object.
# Printing the object itself WON'T work!!!

# simpler for loop: don't use itr = iter(range(len(dataInfo)))
# This is Python, not C!
# If you also need access to the index, use enumerate() to generate a tuple!
# Then you would know where you are in the iteration.
itr = iter(dataInfo)
for i in itr:
    while i == '':
        i = next(itr)
    if circularCount % 3 == 0:
        individualData[count] = float(i)
        if count == 7:
            break
        count += 1
    elif circularCount % 3 == 2:
        totalData = float(i)
    circularCount += 1


# print(info)
# print(numInfo)
# print(dataInfo)
# print(individualData)

# More info on class and scoping:
# https://docs.python.org/3/tutorial/classes.html
class IndividualNumber:
    """A class to store payment info for each individual phone number."""

    def __init__(self, name='', number_string='', number='', shared_charge=0,
                 personal_charge=0, total_charge=0, international=0, insurance=0,
                 installment_status='', installment_charge=0, installment_left=0,
                 data=0, overage=False, overage_charge=0, misc=0):
        self.name = name
        self.number_string = number_string
        self.number = number
        self.shared_charge = shared_charge
        self.personal_charge = personal_charge
        self.total_charge = total_charge
        self.international = international
        self.insurance = insurance
        self.installment_status = installment_status
        self.installment_charge = installment_charge
        self.installment_left = installment_left
        self.data = data
        self.overage = overage
        self.overage_charge = overage_charge
        self.misc = misc

    def print_info(self):
        print('***************************')
        print('Name:\t\t{}'.format(self.name))
        print('Att Number:\t{}'.format(self.number_string))
        #        print(self.number)
        print('Billing Cycle:\t{}'.format(cycleDate))
        print()
        print('Shared Charge:\t\t${}'.format(self.shared_charge))
        print('Personal Charge:\t${}'.format(self.personal_charge))
        print()
        print('Data Usage:\t\t{}GB'.format(self.data))
        if self.overage:
            print('Exceeded Individual Data Quota :(')
            print('Overage Charge:\t\t${}'.format(self.overage_charge))
        else:
            print('No Overage Charge :)')
        print()
        print('Total Charge:\t\t${}'.format(self.total_charge))
        print('\n---------------------------')
        print('Account Detail:')
        print('International Usage:\t${}'.format(self.international))
        print('Insurance & Protection:\t${}'.format(self.insurance))
        print()
        print('Installment Status:\t{}'.format(self.installment_status))
        print('Installment Charge:\t${}'.format(self.installment_charge))
        print('Installment Left:\t${}'.format(self.installment_left))
        print()
        print('Plan Charge & Misc:\t${}'.format(self.misc))
        print()


# Initialize a list of individual number objects for later bookkeeping
numberList = [IndividualNumber() for i in range(accountSize)]

# Request stack
requestStack = list()

# Overall Account Info Bookkeeping
previous = 0
previousFlag = False
amountPaid = 0
amountCollecting = 0

amountSharedFlag = True
amountShared = 0
overageCharge = 0

# Individual User Bookkeeping
count = -1
numberIndices = {}
planBuyerFlag = False

international_i = 0
insurance_i = 0
installmentFlag = False
installmentStatus = 'N/A'
installmentCharge = 0
installmentLeft = 0

itr = iter(info)
for i in itr:
    # print(i)
    # 'is' keyword: identity test; ==: equality test
    # use 'is' for Booleans and identity test
    # use == to compare the internal values
    # Python substring/sublist is [)

    # Generate Information Requests
    if i in ['Previous Balance', 'Total Wireless Charges', 'National Account Discount', 'Data overage billed',
             'Mobile Insurance Premium']:
        requestStack.append(i)
    elif i[:5] == 'Promo' and amountSharedFlag is True:
        requestStack.append(i[:5])
    elif i[:7] == 'Payment' and previousFlag is True:
        requestStack.append(i[:7])
    elif i[:13] == 'International':
        requestStack.append(i[:13])
    elif i[:13] == 'Total Balance':
        if previous - amountPaid == 0:
            print('The Previous Bill Was Paid in Full')
        else:
            print('The Previous Bill Was NOT PAID IN FULL!!! With ${} Left!!!'.format(previous - amountPaid))
        print('\nThis Cycle')
        print('Date:\t{}'.format(cycleDate))
    elif i[:19] == 'Installment Plan ID':
        installmentFlag = True
    elif i[:11] == 'Installment' and installmentFlag is True:
        requestStack.append(i[:11])
        installmentStatus = i[:-1]
        installmentFlag = False
    elif i[:43] == 'Balance Remaining after Current Installment':
        i = i.replace('\n', ' ').replace('\t', '')
        # Balance Remaining after Current Installment:\n\t\t\t\t\t\t$299.99
        # to Balance Remaining after Current Installment: $299.99
        installmentLeft = float(i[46:])
    elif i[:22] == 'Mobile Protection Pack':
        requestStack.append(i[:22])
    # Reach the end of this individual user, generate record!
    elif i[:9] == 'Total for':
        requestStack.append(i[:9])
        count += 1
        numberList[count].number_string = i[10:]
        numberList[count].number = i[10:].replace('-', '')
        numberList[count].name = numberNames[numberList[count].number]
        # map number to its position in numberList
        # So that the data usage can be integrated later
        numberIndices[numberList[count].number] = count

    # Catch Information Request and Pull in Data
    elif (len(i) > 0 and i[0] == '$') or (len(i) > 1 and i[1] == '$'):
        # The latter a replacement for i[:2] == chr(8722) + '$'
        # This will handle both positive and negative numbers
        # Not catching exception: try: except IndexError:
        # IndexError: pop from empty list
        if not requestStack:
            continue
        request = requestStack.pop()
        # Collecting Overall Account Info
        if request == 'Previous Balance':
            previous = float(i[1:])
            previousFlag = True
            print('Previous Cycle')
            print('Previous Balance:\t{}'.format(i))
        elif request == 'Payment':
            amountPaid = float(i[2:])
            previousFlag = False
            print ('Amount Paid:\t\t{}'.format(i))
        elif request == 'Total Wireless Charges':
            amountCollecting = float(i[1:])
            print('Total Data Available:\t{}GB'.format(totalData))
            print('Amount Collecting:\t{}\n'.format(i))
        elif request == 'Data overage billed':
            overageCharge = float(i[1:])
            print ('Data Overage Billed:\t${}'.format(overageCharge))
        elif request == 'Promo':
            amountShared += float(i[1:])
        elif request == 'National Account Discount':
            amountShared -= float(i[2:])
            amountSharedFlag = False
            planBuyerFlag = True
            print ('Amount Shared:\t\t${}'.format(amountShared))

        # Individual Account Info
        elif request == 'International':
            international_i += float(i[1:])
        elif request == 'Mobile Insurance Premium':
            insurance_i += float(i[1:])
        elif request == 'Installment':
            installmentCharge = float(i[1:])
        elif request == 'Mobile Protection Pack':
            insurance_i += float(i[1:])
        elif request == 'Total for':
            numberList[count].shared_charge = amountShared / accountSize
            personalCharge = float(i[1:])
            if planBuyerFlag:
                numberList[count].personal_charge = personalCharge - amountShared - overageCharge
                planBuyerFlag = False
            else:
                numberList[count].personal_charge = personalCharge
            numberList[count].total_charge = numberList[count].shared_charge + numberList[count].personal_charge

            numberList[count].international = international_i
            numberList[count].insurance = insurance_i

            numberList[count].installment_status = installmentStatus
            numberList[count].installment_charge = installmentCharge
            numberList[count].installment_left = installmentLeft
            numberList[count].misc = round(numberList[count].personal_charge - numberList[count].international -
                                           numberList[count].insurance - numberList[count].installment_charge, 2)

            # Initialize ALL the bookkeeping variables for the next user!
            international_i = 0
            insurance_i = 0

            installmentStatus = 'N/A'
            installmentCharge = 0
            installmentLeft = 0

    else:
        continue

# Overage charge needs to be calculated outside of the for loop!
overageCount = 0
for i in range(accountSize):
    if float(individualData[i]) > (totalData / accountSize):
        overageCount += 1
        numberList[numberIndices[numInfo[i]]].overage = True
    numberList[numberIndices[numInfo[i]]].data = float(individualData[i])

for i in numberList:
    if i.overage:
        i.overage_charge = overageCharge / overageCount
        i.total_charge += i.overage_charge

[i.print_info() for i in numberList]

# Correctness Check
sanitySum = round(sum([i.total_charge for i in numberList]), 2)
print('***************************')
print('{} needs to be collected and {} will be collected'.format(amountCollecting, sanitySum))
if sanitySum == amountCollecting:
    print('Charge Sanity Check Passed! :)')
else:
    print('Charge Sanity Check Failed!!! :(')
print('\n***************************')
print('Info Sheet shows the cycle: {}\nand Data Sheet shows: {}'.format(cycleDate, cycleDateFromData))
if cycleDate[:cycleDate.find('-') - 1] == cycleDateFromData[:cycleDateFromData.find(',')]\
        and cycleDate[cycleDate.find('-'):] == cycleDateFromData[cycleDateFromData.find('-'):]:
    print('Date Sanity Check Passed! :)')
else:
    print('Date Sanity Check Failed!!! :(')
