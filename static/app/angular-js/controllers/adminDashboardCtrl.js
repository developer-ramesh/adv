app.controller('adminDashboardCtrl', function($window,$scope,$http,$routeParams,$location,getDashboardService,$filter) {
  $scope.loading = true;
  getDashboardService.getDashboardData().then(function(response){
    $scope.loading = false;
    $scope.dashboardData=response.data.dashboard;
    $scope.permissionData=response.data.permission;

    if(response.data.rolePermission.length==0){
      $window.location.href = '/#/not-permission';
    }else{
      if(jQuery.inArray("View Dashboard", response.data.rolePermission) != -1) {
        //$scope.userRolePermission=response.data.rolePermission;
      } else {
        $window.location.href = '/#/not-permission';
      }
    }

    var roles=response.data.rolePermission;
    if(roles.indexOf('Add Dashboard') !== -1) {
      $scope.add_dashboard='1';
    }else{
      $scope.add_dashboard='';
    }
    if(roles.indexOf("Update Dashboard") !== -1) {
      $scope.update_dashboard='1';
    }else{
      $scope.update_dashboard='';
    }
    if(roles.indexOf("Deactivate Dashboard") !== -1) {
      $scope.deactivate_dashboard='1';
    }else{
      $scope.deactivate_dashboard='';
    }

  });
  $scope.popup_text='Add Dashboard';


  $scope.make_status=function(){
    if($('.dashboard_id').val()!='')
    {
      if (confirm("Are you sure?"))
      {
        $('.ld').css({'display':'inline'}); $('.roll-msg').text('Please wait...');
        getDashboardService.dashboardUpdate($('.dashboard_id').val()).then(function(response){
          if(response.data.status=='success'){
            $scope.status='success';
            $scope.message='Record has been successfully updated';
            setTimeout(function() {
            $scope.status='';
            $scope.$apply();
          }, 3000);
          $('.ld').css({'display':'none'}); $('.roll-msg').text('Deactivate Dashboard');

          $('.table').find('.role-u').each(function(){
            if($(this).val()==$('.dashboard_id').val()){
              $(this).prop( "checked", false );
              $('.dashboard_id').val('');
              $(this).parent().parent().parent().find('.active_stat').text(response.data.msg);
              $(this).parent().parent().parent().find('.updated_by').text(response.data.update_by);
              $(this).parent().parent().parent().find('.updated_date').text($filter('date')(new Date(), 'M/d/yyyy h:mm a'));
            }
          });

          }
        });
      }
    }
    else
    {
      alert('Please choose any Dashboard.');
    }
  }

  $(document).on('click','.role-u',function(){
    $('.dashboard_id').val($(this).val());
  });
  $(document).on('click','#optgroupEdit_leftSelected, #optgroupEdit_rightSelected',function(){
    $('.assign_process option').prop('selected', true);
  });

  $scope.close=function(){
    $scope.popup_text='Add Dashboard';
    $scope.edit_role=''; $scope.asign_process='';
    $scope.dashboard_name='';
    $scope.dashboard_version='';
    $scope.long_name='';
    $scope.help_text='';
  }
  $scope._addDashboard=function(){
    $scope.edit_role='';
    $scope.popup_text='Add Dashboard';
    getDashboardService.getDashboardData().then(function(response){
      $scope.dataProcess=response.data.process;
      $scope.edit_role='11';
      $scope.dash_pic='';
      setTimeout(function(){
        $('#optgroupEdit').multiselect();
      },1000);
    });
  }

  $scope.dashboardFormData=function(){
    $('.assign_process option').prop('selected', true);
    if($('.assign_process').val()!=null){

      var fd = new FormData();
      fd.append("dashboard_name",$('.dashboard_name').val());
      fd.append("long_name",$('.long_name').val());
      fd.append("help_text",$('.help_text').val());
      fd.append("dashboard_version",$('.dashboard_version').val());
      fd.append("dashboard_active",$('.role_active').val());
      fd.append("assign_process",$('.assign_process').val());
      fd.append("dashboard_id",$('.edit_dashboard_id').val());
      fd.append("edit_pic_name",$('.edit_pic_name').val());
      fd.append("file",document.getElementById('pic').files[0]);

      $('.lder').show(); $('.role_save').text('Please wait...');
      getDashboardService.dashboardAdd(fd).then(function(response){
        if(response.data.status=='success'){
          $scope.dashboardData=response.data.dashboard;
          $scope.status_role='success';
          $scope.message_role='Record has been successfully Saved';
          $('.chk').val('');
          $('.role_active').prop( "checked", false );
          $('.assign_process').empty();
          setTimeout(function() {
          $('.btn-default').trigger('click');
          $scope.status_role='';
          $scope.$apply();
        }, 3000);

      }else {
        $scope.status_role='danger';
        $scope.message_role='Sorry, This Dashboard is already exist in database';
        setTimeout(function() {
        $scope.status_role='';
        $scope.$apply();
      }, 5000);
      }
      $('.lder').hide(); $('.role_save').text('Save changes');
      });
    }else{
      alert('Please select Process for Dashboard');
    }
  }


  $scope.editDashboard=function(dashboardID){
    $scope.edit_role='';
    $scope.popup_text='Edit Dashboard';
    getDashboardService.dashboardEdit(dashboardID).then(function(response){
      $scope.edit_role=response.data.dashboard[0];
      $scope.dataProcess=response.data.processP;
      $scope.assigned_process=response.data.user_added_process;
      $scope.dashboard_name=response.data.dashboard[0].fields.short_name;
      $scope.dashboard_version=response.data.dashboard[0].fields.version;
      $scope.long_name=response.data.dashboard[0].fields.long_name;
      $scope.help_text=response.data.dashboard[0].fields.description;
      $scope.dash_pic=response.data.dashboard[0].fields.dashboard_image;
      setTimeout(function(){
    		$('#optgroupEdit').multiselect();
        $('.assign_dashboard option').prop('selected', true);
    	},1000);
    });
  }

  $(document).on('change','#pic',function(event){
    var type = $(this).val().split(".");
    ext=type.pop();
    if(ext!='jpg' && ext!='png'){
      $(this).val('');
      $('#pic').val('');
      $('#pic').addClass('err');
      alert('Please choose valid file.');
    }else{
      $('#pic').removeClass('err');
    }
  });

});
