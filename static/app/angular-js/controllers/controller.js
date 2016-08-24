/*********************** Below Controller for Administration Import data*************************
************************          Start              *************************/

app.controller('adminDataCtrl', function($window,$scope,$http,$routeParams,$location, getAdministrationData) {

  $scope.loading = true;
  getAdministrationData.getData().then(function(response){

    if(response.data.rolePermission.length==0){
      $window.location.href = '/#/not-permission';
    }

    var roles=response.data.rolePermission;
    if(roles.indexOf('Rollback Data') !== -1) {
      $scope.rollback='1';
    }else{
      $scope.rollback='';
    }

    if(roles.indexOf('Upload Data') !== -1) {
      $scope.upload_data='1';
    }else{
      $scope.upload_data='';
    }


    $scope.dataType=response.data.DataType;
    $scope.compData=response.data.compData;
    $scope.UserCompId=response.data.UserCompId;
    $scope.logData=response.data.logData;
    if(response.data.DataType!=''){
      $('.no-record').remove();
      $scope.loading = false;
      setTimeout(function() {
        $('.data_type option[value="Invoices"]').remove();
        $('.data_type option[value="Payments"]').remove();
        $('.data_type option[value="Purchase Orders"]').remove();
        $('.pagination').find('li:first-child > a ').text('First');
        $('.pagination').find('li:last-child > a ').text('Last');
      }, 1000);

    }
  });


  $scope.dataImport=function(){
    if($('.data_type').val() && $('#upload-file-info').val()!=''){
    var fd = new FormData();
    fd.append("data_type",$('.data_type').val());
    fd.append("comp_id",$('.comp_name').val());
    fd.append("comp_name",$('.comp_name').text().trim());
    fd.append("file",document.getElementById('my-file-selector').files[0]);

    var fd1 = new FormData();
    fd1.append("data_type",$('.data_type').val());
    fd1.append("comp_id",$('.comp_name').val());
    fd1.append("comp_name",$('.comp_name').text().trim());

    getAdministrationData.importData(fd).then(function(response){
      $scope.logData=response.data.logData;
      fd1.append("file_name",response.data.file_name);
      fd1.append("upload_id",response.data.upload_id);
      console.log(response);
      if(response.data.status=='success'){
          getAdministrationData.importDataStep2(fd1).then(function(step2){
            console.log(step2);
              if(step2.data.status=='success'){
                $('.table-wrap table tbody tr:first-child td.status').text('2 of 6 File Formate Check');
                getAdministrationData.importDataStep3(fd1).then(function(step3){
                   console.log(step3);
                   if(step3.data.status=='success'){
                     $('.table-wrap table tbody tr:first-child td.status').text('4 of 6 Duplicate Check');
                     getAdministrationData.importDataStep5(fd1).then(function(step5){
                       console.log(step5);
                       if(step5.data.status=='success'){
                         $('.table-wrap table tbody tr:first-child td.status').text('5 of 6 Master Update Done');
                         $('.table-wrap table tbody tr:first-child td.no_records').text(step5.data.chk);
                         getAdministrationData.importDataStep6(fd1).then(function(step6){
                           console.log(step6);
                           $('.table-wrap table tbody tr:first-child td.status').text(step6.data.message);
                           $scope.status=step6.data.status;
                           $scope.message='Records has been success uploaded.';
                           $scope.logData=step6.data.logData;
                           $('.upload-btn').val('Upload Data');
                           $('.ldr').hide();
                         });
                       }else{
                         $('.table-wrap table tbody tr:first-child td.status').text('5 of 6 Master Update Error');
                         $('.table-wrap table tbody tr:first-child td.no_records').text(step5.data.chk);
                         $scope.status=step5.data.status;
                         $scope.message=step5.data.message;
                         $('.upload-btn').val('Upload Data');
                         $('.ldr').hide();
                       }
                     });
                   }
                   else{
                     $('.table-wrap table tbody tr:first-child td.status').text('5 of 6 Master Update');
                     $('.table-wrap table tbody tr:first-child td.no_records').text(step5.data.chk);
                     $scope.status=step3.data.status;
                     $scope.message=step3.data.message;
                     $('.upload-btn').val('Upload Data');
                     $('.ldr').hide();
                   }
                });

              }else{
                $scope.status=step2.data.status;
                $scope.message=step2.data.message;
                $('.upload-btn').val('Upload Data');
                $('.ldr').hide();
              }
          });
      }
      // $scope.status=response.data.status;
      // $scope.message=response.data.message;
      // $scope.logData=response.data.logData;
      // $('.upload-btn').val('Upload Data');
      // $('.ldr').hide();
      // if(response.data.status=='success'){
      //   $('.cancel-btn').trigger('click');
      // }



    });
  }
}

$scope.get_log_data=function(upid){
  $scope.log_details='';
  getAdministrationData.get_data_log(upid).then(function(response){
    if(response.data.log.length!=0){
        $scope.log_details=response.data.log;
    }else{
      $('.log-no').html('No Records');
    }
  });
}

/*
$scope.cancel=function(){
  $http.get('/del-file').success(function(data) {
    console.log(data);
  });
}*/

$scope.__rollback=function(){
  if($('.data_upload_id').val()!=''){
    var fd = $('.data_upload_type').val()+'-'+$('.data_upload_id').val()
    $('.rollback-loader').css({'display':'inline'});$('.roll').text('Please wait...');
    $http({method:'POST',url:'/roll-back/',data:fd, headers : {'Content-Type': 'application/x-www-form-urlencoded'}}).success(function(response) {
      if(response.status!=''){

        check_status('1 of 3 Rollback In Progress');

        $http({method:'POST',url:'/roll-back2/',data:fd, headers : {'Content-Type': 'application/x-www-form-urlencoded'}}).success(function(response2) {
            if(response2.status!=''){

              setTimeout(function() {
              check_status('2 of 3 Master Updates In Progress');
            },2000);

              $http({method:'POST',url:'/roll-back3/',data:fd, headers : {'Content-Type': 'application/x-www-form-urlencoded'}}).success(function(response3) {
                  if(response3.status!=''){

                    setTimeout(function() {
                    check_status('3 of 3 Rollback Done');
                    $scope.status=response3.status;
                    $scope.message='Rollbacked has been successfully';
                    $('.rollback-loader').css({'display':'none'}); $('.roll').text('Rollback Data');
                  },3000);
                  }
              });

            }else{
              $scope.status=response.status;
              $scope.message=response.message;
              $('.rollback-loader').css({'display':'none'}); $('.roll').text('Rollback Data');
            }
        });

      }else {
        $scope.status=response.status;
        $scope.message=response.message;
        $('.rollback-loader').css({'display':'none'}); $('.roll').text('Rollback Data');
      }
    });
  }else{
    alert('Please choose any record to Rollback data.');
  }
}



function check_status(msg){
  $('.table').find('.datauplid').each(function(){
    if($(this).val()==$('.data_upload_id').val()){
      $(this).hide();
      $(this).parent().parent().find('.status').text(msg);
    }
  });
}

});

/*********************** Above Controller for Administration Import data *************************
************************          End              *************************/



/*********************** Below Controller for Administration Audit Log*************************
************************          Start              *************************/

app.controller('adminAuditLogCtrl', function($window,$scope,$http,$routeParams,$location,getAdminAuditLog) {
  $scope.loading = true;
  getAdminAuditLog.getLogData().then(function(response){

    if(response.data.rolePermission.length==0){
      $window.location.href = '/#/not-permission';
    }

    $scope.eventCategory=response.data.eventCategory;
    $scope.eventSubCategory=response.data.eventSubCategory;
    $scope.eventType=response.data.eventType;
    $scope.compData=response.data.compData;
    $scope.UserCompId=response.data.UserCompId;
    if(response.data.eventCategory!=''){
      $('.no-record').remove();
      $scope.loading = false;
    }
  });



  $scope.searchFilter=function(){
    $scope.loading = true;
    getAdminAuditLog.searchAuditLog($('.frm').serialize()).then(function(response){
      $scope.logData=response.data.logData;
      $scope.expt_file_name=response.data.expt_file_name;
      $scope.loading = false;
      if(response.data.logData.length!=0){
        setTimeout(function() {
        $('.pagination').find('li:first-child > a ').text('First');
        $('.pagination').find('li:last-child > a ').text('Last');
        },1000);
        $('.alert-warning').remove();
      }else{
        $('.alert-warning').remove();
        $('.searchFrm').after('<div class="alert alert-warning" role="alert">No record found!!!</div>');
      }
    });
  }

  $scope.changeItem=function(itm){
    $('.sub_act').hide(); $('.loader').show();
    $http({method:'POST',url:'/get-event-subcategory/',data:itm, headers : {'Content-Type': 'application/x-www-form-urlencoded'}}).success(function(response) {
      $scope.eventSubCategory=response.subCategory;
        $('.sub_act').show(); $('.loader').hide();
    });
  }

  $(document).on('click','.back_to_search',function(){
    setTimeout(function() {
    $scope.logData = '';
    $scope.$apply();
    }, 500);
  });

});
/*********************** Above Controller for Administration Audit Log*************************
************************          End              *************************/

app.controller('notPermitCtrl', function($window,$scope,$http,$routeParams,$location) {

});
