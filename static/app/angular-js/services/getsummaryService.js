app.factory('getsummaryService', function ($http) {

  return {
      getSummaryData : function(){
        return $http.get('/get-summary-data')
        .success(function(data) {});
      },
      searchSummaryData : function(params){
      //return $http.post('/get-summary-data/', {'dat':params} )
      return $http({method:'POST',url:'/get-summary-data/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      }
    }

});


app.factory('getDuplicateService', function ($http) {

  return {
      getSummaryData : function(){
        return $http.get('/get-duplicate-data')
        .success(function(data) {});
      },
      searchSummaryData : function(params){
      //return $http.post('/get-duplicate-data/', {'dat':params} )
      return $http({method:'POST',url:'/get-duplicate-data/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      }
    }

});
