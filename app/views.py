from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from .models import Employee, PayStatement, PayrollAccount

def index(request):
    template = loader.get_template('app/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def statement(request, statementId):
    try:
        payStatement = model_to_dict(PayStatement.objects.get(id=statementId))
        employeeObject = Employee.objects.get(id=payStatement['employee'])
        yearStart = '{}-01-01'.format(payStatement['payDate'].year)
        payStatementsForTheYear = PayStatement.objects.filter(employee=employeeObject, payDate__range=(yearStart, payStatement['payDate']))
    except:
        return HttpResponseNotFound("Pay Statement {} does not exist".format(statementId))

    for dateField in ['payPeriodStart', 'payPeriodEnd', 'payDate']:
        payStatement[dateField] = str(payStatement[dateField])
    
    employee = model_to_dict(employeeObject)
    payrollAccount = model_to_dict(PayrollAccount.objects.get(id=employee['payrollAccount']))

    payStatement.update(employee)
    payStatement['payrollAccountName'] = payrollAccount['name']

    payStatement['grossPay'] = payStatement['regularPay'] + payStatement['vacationPay']
    payStatement['deductions'] = payStatement['federalIncomeTax'] + payStatement['provincialIncomeTax'] + payStatement['ei'] + payStatement['cpp']
    payStatement['netPay'] = payStatement['grossPay'] - payStatement['deductions']

    payStatement['regularPayYtd'] = 0
    payStatement['vacationPayYtd'] = 0
    payStatement['federalIncomeTaxYtd'] = 0
    payStatement['provincialIncomeTaxYtd'] = 0
    payStatement['eiYtd'] = 0
    payStatement['eiEmployerYtd'] = 0
    payStatement['cppYtd'] = 0
    payStatement['cppEmployerYtd'] = 0
    payStatement['grossPayYtd'] = 0
    payStatement['deductionsYtd'] = 0
    payStatement['netPayYtd'] = 0

    for statementWithinYear in payStatementsForTheYear:
        grossPay = statementWithinYear.regularPay + statementWithinYear.vacationPay
        deductions = statementWithinYear.federalIncomeTax + statementWithinYear.provincialIncomeTax + statementWithinYear.ei + statementWithinYear.cpp
        netPay = grossPay - deductions

        payStatement['regularPayYtd'] += statementWithinYear.regularPay
        payStatement['vacationPayYtd'] += statementWithinYear.vacationPay
        payStatement['federalIncomeTaxYtd'] += statementWithinYear.federalIncomeTax
        payStatement['provincialIncomeTaxYtd'] += statementWithinYear.provincialIncomeTax
        payStatement['eiYtd'] += statementWithinYear.ei
        payStatement['eiEmployerYtd'] += statementWithinYear.eiEmployer
        payStatement['cppYtd'] += statementWithinYear.cpp
        payStatement['cppEmployerYtd'] += statementWithinYear.cppEmployer
        payStatement['grossPayYtd'] += grossPay
        payStatement['deductionsYtd'] += deductions
        payStatement['netPayYtd'] += netPay

    moneyFields = [
        'hourlyWage', 'regularPay', 'vacationPay', 'regularPayYtd', 'vacationPayYtd', 
        'federalIncomeTax', 'federalIncomeTaxYtd', 'provincialIncomeTax', 'provincialIncomeTaxYtd', 
        'ei', 'eiYtd', 'eiEmployer', 'eiEmployerYtd', 'cpp', 'cppYtd', 'cppEmployer', 'cppEmployerYtd', 
        'grossPay', 'deductions', 'netPay', 'grossPayYtd', 'deductionsYtd', 'netPayYtd'
    ]

    for moneyField in moneyFields:
        payStatement[moneyField] = '{:.2f}'.format(payStatement[moneyField])

    payStatement['employeeNumber'] = '{:04d}'.format(payStatement['employeeNumber'])

    template = loader.get_template('app/statement.html')
    return HttpResponse(template.render(payStatement, request))

@require_http_methods(["POST"])
def employees(request):
    employees = list(Employee.objects.all().values())
    return JsonResponse({"employees": employees})

@require_http_methods(["POST"])
def paystatements(request):
    payStatements = list(PayStatement.objects.all().values())
    return JsonResponse({"payStatements": payStatements})

@require_http_methods(["POST"])
def paysubmission(request):
    employee = Employee.objects.get(id=request.POST['employeeId'])
    payStatement = PayStatement(
        employee=employee,
        payPeriodStart=request.POST['payPeriodStart'],
        payPeriodEnd=request.POST['payPeriodEnd'],
        payDate=request.POST['payDate'],
        payFrequency=request.POST['payFrequency'],
        payHours=request.POST['payHours'],
        regularPay=request.POST['regularPay'],
        vacationPay=request.POST['vacationPay'],
        federalIncomeTax=request.POST['federalIncomeTax'],
        provincialIncomeTax=request.POST['provincialIncomeTax'],
        ei=request.POST['ei'],
        cpp=request.POST['cpp'],
        eiEmployer=request.POST['eiEmployer'],
        cppEmployer=request.POST['cppEmployer'],
    )
    payStatement.save()
    return JsonResponse({})
