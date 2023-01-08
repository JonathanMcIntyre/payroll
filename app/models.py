from django.db import models

class PayrollAccount(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)

class Employee(models.Model):
    payrollAccount = models.ForeignKey(PayrollAccount, on_delete=models.CASCADE)
    employeeNumber = models.IntegerField()
    firstName = models.CharField(max_length=64)
    middleName = models.CharField(max_length=64, blank=True, default='')
    lastName = models.CharField(max_length=64)
    jobTitle = models.CharField(max_length=64)
    streetAddress = models.CharField(max_length=255)
    city = models.CharField(max_length=32)
    province = models.CharField(max_length=16)
    postalCode = models.CharField(max_length=8)
    country = models.CharField(max_length=32)
    hourlyWage = models.FloatField()

    def __str__(self):
        return '{} {}'.format(self.firstName, self.lastName)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['payrollAccount', 'employeeNumber'], name='Unique Employee Constraint')
        ]

class PayStatement(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payPeriodStart = models.DateField()
    payPeriodEnd = models.DateField()
    payDate = models.DateField()
    payFrequency = models.CharField(max_length=64)
    payHours = models.FloatField()
    regularPay = models.FloatField()
    vacationPay = models.FloatField()
    federalIncomeTax = models.FloatField()
    provincialIncomeTax = models.FloatField()
    ei = models.FloatField()
    cpp = models.FloatField()
    eiEmployer = models.FloatField()
    cppEmployer = models.FloatField()

    def __str__(self):
        grossPay = self.regularPay + self.vacationPay
        deductions = self.federalIncomeTax + self.provincialIncomeTax + self.ei + self.cpp
        netPay = grossPay - deductions
        return '{} - {} - Net Pay: ${:.2f}'.format(self.employee, self.payDate, netPay)
