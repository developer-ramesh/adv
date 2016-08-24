app.factory('getUserService', function ($http) {

  return {
      getUserData : function(){
        return $http.get('/get-user')
        .success(function(data) {});
      },
      userAdd : function(params){
      return $http({method:'POST',url:'/get-user/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
      .success(function(data) {});
      },
      userAssignDataAdd : function(params){
      return $http({method:'POST',url:'/add-user-assign_data/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
      .success(function(data) {});
      },
      userAssignData : function(params){
      return $http({method:'POST',url:'/get-assign_data/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
      .success(function(data) {});
      },
      userUpdate : function(params){
      return $http({method:'POST',url:'/user-status/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      }
    }

});

app.factory('getMessageService', function ($http) {

  return {
      getMessageData : function(){
        return $http.get('/get-message')
        .success(function(data) {});
      },
      messagedAdd : function(params){
      return $http({method:'POST',url:'/get-message/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
      .success(function(data) {});
      },
      messageEdit : function(params){
      return $http({method:'POST',url:'/edit-message/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      },
      messageUpdate : function(params){
      return $http({method:'POST',url:'/message-status/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      }
    }

});

app.factory('getCompanyService', function ($http) {

  return {
      getCompanyData : function(){
        return $http.get('/get-company')
        .success(function(data) {});
      },
      companyAdd : function(params){
      return $http({method:'POST',url:'/get-company/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
      .success(function(data) {});
      },
      companyEdit : function(params){
      return $http({method:'POST',url:'/edit-company/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      },
      companyUpdate : function(params){
      return $http({method:'POST',url:'/company-status/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      },
      companyLicense : function(params){
      return $http({method:'POST',url:'/company-licenses/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
    },
    companyLicenseUpdate : function(params){
    return $http({method:'POST',url:'/company-licenses-update/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
    .success(function(data) {});
    },
    companyDashboards : function(params){
    return $http({method:'POST',url:'/company-dashboard/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
    .success(function(data) {});
    },
    companyDashboardsUpdate : function(params){
    return $http({method:'POST',url:'/company-dashboard-update/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
    .success(function(data) {});
    }
    }

});

app.factory('getDashboardService', function ($http) {

  return {
      getDashboardData : function(){
        return $http.get('/get-dashboard')
        .success(function(data) {});
      },
      dashboardAdd : function(params){
      return $http({method:'POST',url:'/get-dashboard/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
      .success(function(data) {});
      },
      dashboardEdit : function(params){
      return $http({method:'POST',url:'/edit-dashboard/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      },
      dashboardUpdate : function(params){
      return $http({method:'POST',url:'/dashboard-status/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      }
    }

});

app.factory('getProcessService', function ($http) {

  return {
      getProcessData : function(){
        return $http.get('/get-process')
        .success(function(data) {});
      },
      processAdd : function(params){
      return $http({method:'POST',url:'/get-process/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
      .success(function(data) {});
      },
      processEdit : function(params){
      return $http({method:'POST',url:'/edit-process/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      },
      processUpdate : function(params){
      return $http({method:'POST',url:'/process-status/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      }
    }

});

app.factory('getRoleService', function ($http) {

  return {
      getRolesData : function(){
        return $http.get('/get-roles')
        .success(function(data) {});
      },
      roleAdd : function(params){
      return $http({method:'POST',url:'/get-roles/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      },
      roleEdit : function(params){
      return $http({method:'POST',url:'/edit-role/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      },
      roleUpdate : function(params){
      return $http({method:'POST',url:'/role-status/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
      }
    }

});

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


app.factory('getHighDollerService', function ($http) {

  return {
      getData : function(type){
        return $http.get('/get-highdoller-data?dashboardType='+type)
        .success(function(data) {});
      },
      searchData : function(params,type){
      return $http({method:'POST',url:'/get-highdoller-data/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
    },
    getDetailRecords : function(params,type){
    return $http({method:'POST',url:'/get-detail-records/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
    .success(function(data) {});
    }
    }

});



/*** Start This is for Admin data Import data from excel file  ****/
app.factory('getAdministrationData', function ($http) {

  return {
      getData : function(){
        return $http.get('/upload-employee-data')
        .success(function(data) {});
      },
      importData : function(params){
      return $http({method:'POST',url:'/upload-employee-data/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
      .success(function(data) {});
    },
    importDataStep2 : function(params){
    return $http({method:'POST',url:'/upload-employee-data-step2/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
    .success(function(data) {});
  },
    importDataStep3 : function(params){
    return $http({method:'POST',url:'/upload-employee-data-step3/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
    .success(function(data) {});
  },
    importDataStep5 : function(params){
    return $http({method:'POST',url:'/upload-employee-data-step5/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
    .success(function(data) {});
  },
  importDataStep6 : function(params){
  return $http({method:'POST',url:'/upload-employee-data-step6/',data:params,headers : {'Content-Type': undefined},transformRequest: angular.identity, withCredentials: true })
  .success(function(data) {});
},
get_data_log : function(params){
return $http({method:'POST',url:'/get-data-log/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
.success(function(data) {});
}
}

});
/*** End This is for Admin data Import data from excel file  ****/


/*** Start This is for Admin Audit Data  ****/
app.factory('getAdminAuditLog', function ($http) {
  return {
      getLogData : function(){
        return $http.get('/audit-log')
        .success(function(data) {});
      },
      searchAuditLog : function(params){
      return $http({method:'POST',url:'/audit-log/',data:params,headers : {'Content-Type': 'application/x-www-form-urlencoded'} })
      .success(function(data) {});
    }
    }
});
/*** End This is for Admin Audit Data  ****/
