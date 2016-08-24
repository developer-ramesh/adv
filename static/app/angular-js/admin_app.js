  var app = angular.module("myapp", ['ngRoute','angularUtils.directives.dirPagination']);

  app.config(function ($routeProvider, $locationProvider) {
        $routeProvider
        .when('/administration/user/', {controller  : 'adminUserCtrl', controllerAs: 'adminUserCtrl' ,templateUrl :'/static/app/templates/admin/administration_user.html'})
        .when('/administration/message/', {controller  : 'adminMessageCtrl', controllerAs: 'adminMessageCtrl' ,templateUrl :'/static/app/templates/admin/administration_message.html'})
        .when('/administration/company/', {controller  : 'adminCompanyCtrl', controllerAs: 'adminCompanyCtrl' ,templateUrl :'/static/app/templates/admin/administration_company.html'})
        .when('/administration/dashboard/', {controller  : 'adminDashboardCtrl', controllerAs: 'adminDashboardCtrl' ,templateUrl :'/static/app/templates/admin/administration_dashboard.html'})
        .when('/administration/process/', {controller  : 'adminProcessCtrl', controllerAs: 'adminProcessCtrl' ,templateUrl :'/static/app/templates/admin/administration_process.html'})
        .when('/administration/role/', {controller  : 'adminRoleCtrl', controllerAs: 'adminRoleCtrl' ,templateUrl :'/static/app/templates/admin/administration_role.html'})
        .when('/duplicate-purchase-orders', {controller  : 'duplicpurchordersCtrl', controllerAs: 'duplicpurchordersCtrl' ,templateUrl :'/static/app/templates/admin/duplicate-purchase-orders.html'})
        .when('/summary-spend', {controller  : 'summaryspendCtrl', controllerAs: 'summaryspendCtrl' ,templateUrl :'/static/app/templates/admin/summary-spend.html'})
        .when('/high-risk-merchant-categories', {controller  : 'highriskmerchantcatCtrl', controllerAs: 'highriskmerchantcatCtrl' ,templateUrl :'/static/app/templates/admin/high-risk-merchant-categ.html'})
        .when('/daily-meals-over-threshold', {controller  : 'dailymealsCtrl', controllerAs: 'dailymealsCtrl' ,templateUrl :'/static/app/templates/admin/daily-meals-over-threshold.html'})
        .when('/personal-meals-over-threshold', {controller  : 'personalmealsCtrl', controllerAs: 'personalmealsCtrl' ,templateUrl :'/static/app/templates/admin/personal-meals-over-threshold.html'})
        .when('/excessive-high-risk-expense-categories', {controller  : 'excessiveHighRiskExpenseCtrl', controllerAs: 'excessiveHighRiskExpenseCtrl' ,templateUrl :'/static/app/templates/admin/excessive-high-risk-expense.html'})
        .when('/suspicious-keywords', {controller  : 'suspiciousKeywordsCtrl', controllerAs: 'suspiciousKeywordsCtrl' ,templateUrl :'/static/app/templates/admin/suspicious-Keyword.html'})
        .when('/high-mileage', {controller  : 'highmileageCtrl', controllerAs: 'highmileageCtrl' ,templateUrl :'/static/app/templates/admin/high-mileage.html'})
        .when('/high-dollar', {controller  : 'highdollarCtrl', controllerAs: 'highdollarCtrl' ,templateUrl :'/static/app/templates/admin/high-dollar.html'})
        .when('/not-permission', {controller  : 'notPermitCtrl', controllerAs: 'notPermitCtrl' ,templateUrl :'/static/app/templates/not-permission.html'})
        .when('/administration/audit-log/', {controller  : 'adminAuditLogCtrl', controllerAs: 'adminAuditLogCtrl' ,templateUrl :'/static/app/templates/admin/administration_audit_log.html'})
        .when('/administration/data/', {controller  : 'adminDataCtrl', controllerAs: 'adminDataCtrl' ,templateUrl :'/static/app/templates/admin/administration_data.html'})
        .when('/summary', {controller  : 'summaryCtrl', controllerAs: 'summaryCtrl' ,templateUrl :'/static/app/templates/admin/index.html'})
        .when('/duplicate', {controller  : 'duplicateCtrl', controllerAs: 'duplicateCtrl' ,templateUrl :'/static/app/templates/admin/duplicate.html'})
        .when('/', {controller  : 'summaryCtrl', controllerAs: 'summaryCtrl' ,templateUrl :'/static/app/templates/admin/index.html'})
        .otherwise({ redirectTo: '/summary/' });
        //$locationProvider.html5Mode(true);
  });

  // set the configuration
  app.run(['$rootScope', function($rootScope,$http){
    //$rootScope.dir = path.url;
    //$rootScope.site = path.site;
  }]);

  app.filter('nfcurrency', [ '$filter', '$locale', function ($filter, $locale) {
    var currency = $filter('currency'), formats = $locale.NUMBER_FORMATS;
    return function (amount, symbol) {
        var value = currency(amount, symbol);
        return value.replace(new RegExp('\\' + formats.DECIMAL_SEP + '\\d{2}'), '')
    }
}]);
