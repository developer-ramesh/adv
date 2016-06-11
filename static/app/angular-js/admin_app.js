  var app = angular.module("myapp", ['ngRoute']);

  app.config(function ($routeProvider, $locationProvider) {
        $routeProvider
        .when('/expenses/summary', {controller  : 'summaryCtrl', controllerAs: 'summaryCtrl' ,templateUrl :'/static/app/templates/admin/index.html'})
        .when('/expenses/duplicate/details', {controller  : 'duplicateDetailsCtrl', controllerAs: 'duplicateDetailsCtrl' ,templateUrl :'/static/app/templates/admin/duplicate_details.html'})
        .when('/expenses/duplicate', {controller  : 'duplicateCtrl', controllerAs: 'duplicateCtrl' ,templateUrl :'/static/app/templates/admin/duplicate.html'})
        .when('/', {controller  : 'summaryCtrl', controllerAs: 'summaryCtrl' ,templateUrl :'/static/app/templates/admin/index.html'})
        .otherwise({ redirectTo: '/expenses/summary/' });
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
