app.controller('summaryCtrl', function($scope,$http,$routeParams,$location, getsummaryService) {
    $scope.loading = true;
    var title = $location.path();
    
    currency_type='$';
    $scope.viewBy='';
    $('.viewBy').change(function(){
      var vb = $(this).val();
      setTimeout(function() {
      return $scope.viewBy = vb;
      $scope.$apply();
      }, 500);

      if(vb=='transaction_amount'){
        return currency_type='$';
      }else{
        return currency_type='';
      }
    }).blur();

    getsummaryService.getSummaryData().then(function(response){
      if(response.data.JobStatistics.length!=0){
        $('.no-record').remove();
      }
      else{
        $('.left-panel').after('<div class="no-record visible-lafepan"><div class="err-txt"><i class="fa fa-meh-o"></i><span>OOPS!</span>No record found...</div></div>');
      }

      $scope.country_data=response.data.GraphCountries;
      $scope.expense_type_data=response.data.Categories_list;
      $scope.function_name_data=response.data.functionItems;
      $scope.fiscal_data=response.data.QuarterItems;
      $scope.spend_cat_data=response.data.GraphCategories;
      $scope.paymentType=response.data.paymentType

      $scope.employee_name_data=response.data.Employee;
      $scope.department_name_data=response.data.Department;
      $scope.countries_data=response.data.GraphCountries;
      $scope.exjobstatics=response.data.JobStatistics[0];
      $scope.bucket_data=response.data.BucketAnalysis;
      $scope.max_val =Math.max.apply(Math,response.data.BucketAnalysis.map(function(item){return item.expenses;}));
      $scope.dataLeft = response.data.dataLeft;
      $scope.loading = false;

      setTimeout(function(){
        $('.count').Jcount_data();
        $('.multi-select').multiselect();
        $('#by-month').JchartByMonth(response.data.GraphMonth,response.data.PaymentMonth,currency_type, response.data.GraphCategories,response.data.Categories_list,response.data.GraphCountries);
    		$(".custom-scroller").mCustomScrollbar({ theme:"dark-thin", scrollbarPosition:"inside" });
      },1000);

    });




    /*********************** Below function for Filter *************************
    ************************          Start            ************************/

    $scope.searchFilter=function(){

      $scope.loading = true;
      getsummaryService.searchSummaryData($('.frm').serialize()).then(function(responseData){
        if(responseData.data.JobStatistics.length!=0){
          $('.no-record').remove();
        }else{
          $('.left-panel').after('<div class="no-record visible-lafepan"><div class="err-txt"><i class="fa fa-meh-o"></i><span>OOPS!</span>No record found...</div></div>');
        }
        $scope.viewBy=$scope.viewBy;
        if(responseData.data.DataType=='search'){
          $scope.exjobstatics=responseData.data.JobStatistics[0];
        }else if(responseData.data.Type=='normal'){
          $scope.exjobstatics=responseData.data.JobStatistics[0];
        }

        $scope.max_val =Math.max.apply(Math,responseData.data.BucketAnalysis.map(function(item){return item.expenses;}));

        $scope.employee_name_data=responseData.data.Employee;
        $scope.department_name_data=responseData.data.Department;
        $scope.countries_data=responseData.data.GraphCountries;
        $scope.bucket_data=responseData.data.BucketAnalysis;
        $scope.loading = false;

        $scope.country_data=responseData.data.GraphCountries;
        $scope.expense_type_data=responseData.data.Categories_list;
        $scope.function_name_data=responseData.data.functionItems;
        $scope.fiscal_data=responseData.data.QuarterItems;
        $scope.spend_cat_data=responseData.data.GraphCategories;

        setTimeout(function(){
          $('.count').Jcount_data();
          $('.multi-select').multiselect('refresh');
          $('#by-month').JchartByMonth(responseData.data.GraphMonth,responseData.data.PaymentMonth,currency_type, responseData.data.GraphCategories,responseData.data.Categories_list,responseData.data.GraphCountries);
      		$(".custom-scroller").mCustomScrollbar({ theme:"dark-thin", scrollbarPosition:"inside" });
        },1000);

      });

    }
    /*********************** Above function for Filter *************************
    ************************          End              *************************/

});
