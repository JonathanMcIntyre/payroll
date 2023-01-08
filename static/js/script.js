const VACATION_PAY_RATE = 0.04;
const EI_EMPLOYER_MATCH_RATE = 1.4;
var employees = [];
var payStatements = [];

function employeesSuccess(data) {
  employees = data.employees;
  employees.forEach(employee => {
    $("#employee-select").append($("<option>", {
      value: employee.id,
      text: `${employee.firstName} ${employee.lastName}`
    }));
  });

  $("#job-title").val(employees[0].jobTitle);
  $("#hourly-wage").val(employees[0].hourlyWage);
}

function getEmployees() {
  postData("/app/employees", {}, employeesSuccess);
}

function paystatementsSuccess(data) {
  payStatements = data.payStatements;
  $('#pay-statements').empty()
  payStatements.slice().reverse().forEach(payStatement => {
    $("#pay-statements").append($("<option>", {
      value: payStatement.id,
      text: `${payStatement.payPeriodStart} to ${payStatement.payPeriodEnd}`
    }));
  });
}

function getPayStatements() {
  postData("/app/paystatements", {}, paystatementsSuccess);
}

function moneyRound(num) {
  return Math.ceil(num * 100) / 100;
}

function calculatePay() {
  const payHours = $("#pay-hours").val();
  const hourlyWage = $("#hourly-wage").val();
  const regularPay = moneyRound(payHours * hourlyWage);
  const vacationPay = moneyRound(regularPay * VACATION_PAY_RATE);

  $("#regular-pay").val(regularPay);
  $("#vacation-pay").val(vacationPay);
  $("#gross-pay").val(regularPay + vacationPay);
}

function matchCpp() {
  $("#cpp-employer").val($("#cpp").val());
}

function matchEi() {
  $("#ei-employer").val(moneyRound(EI_EMPLOYER_MATCH_RATE * $("#ei").val()));
}

function submitPayStatementSuccess(data) {
  getPayStatements();
}

function submitPayStatement() {
  const data = {
    employeeId: $("#employee-select").val(),
    payPeriodStart: $("#pay-period-start").val(),
    payPeriodEnd: $("#pay-period-end").val(),
    payDate: $("#pay-date").val(),
    payFrequency: $("#pay-frequency").val(),
    payHours: $("#pay-hours").val(),
    regularPay: $("#regular-pay").val(),
    vacationPay: $("#vacation-pay").val(),
    federalIncomeTax: $("#federal-income-tax").val(),
    provincialIncomeTax: $("#provincial-income-tax").val(),
    ei: $("#ei").val(),
    cpp: $("#cpp").val(),
    eiEmployer: $("#ei-employer").val(),
    cppEmployer: $("#cpp-employer").val(),
  }

  postData("/app/paysubmission", data, submitPayStatementSuccess);
}

function openPayStatement() {
  window.open('/app/statement/' + $('#pay-statements').val(), '_blank').focus();
}

function fillFromStatement() {
  const statement = payStatements.find(payStatement => payStatement.id === +$('#pay-statements').val());
  $("#pay-period-start").val(statement.payPeriodStart);
  $("#pay-period-end").val(statement.payPeriodEnd);
  $("#pay-date").val(statement.payDate);
  $("#pay-frequency").val(statement.payFrequency);
  $("#pay-hours").val(statement.payHours);
  $("#regular-pay").val(statement.regularPay);
  $("#vacation-pay").val(statement.vacationPay);
  $("#gross-pay").val(statement.regularPay + statement.vacationPay);
  $("#federal-income-tax").val(statement.federalIncomeTax);
  $("#provincial-income-tax").val(statement.provincialIncomeTax);
  $("#ei").val(statement.ei);
  $("#cpp").val(statement.cpp);
  $("#ei-employer").val(statement.eiEmployer);
  $("#cpp-employer").val(statement.cppEmployer);
}

getEmployees();
getPayStatements();
