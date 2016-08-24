app.controller('adminUserCtrl', function($window,$scope,$http,$routeParams,$location,getUserService,$filter) {
  $scope.loading = true;
  getUserService.getUserData().then(function(response){
    $scope.loading = false;
    $scope.userData=response.data.users;
    $scope.compData=response.data.compData;
    $scope.UserCompId=response.data.UserCompId;
    if(response.data.rolePermission.length==0){
      $window.location.href = '/#/not-permission';
    }else{
      if(jQuery.inArray("View User", response.data.rolePermission) != -1) {
      } else {
        $window.location.href = '/#/not-permission';
      }
    }


    var roles=response.data.rolePermission;
    if(roles.indexOf("Add User") !== -1) {
      $scope.add_user='1';
    }else{
      $scope.add_user='';
    }
    if(roles.indexOf("Update User") !== -1) {
      $scope.update_user='1';
    }else{
      $scope.update_user='';
    }
    if(roles.indexOf("Deactivate User") !== -1) {
      $scope.deactivate_user='1';
    }else{
      $scope.deactivate_user='';
    }
    if(roles.indexOf("Assign Processes") !== -1) {
      $scope.assign_process='1';
    }else{
      $scope.assign_process='';
    }
    if(roles.indexOf("Assign Roles") !== -1) {
      $scope.assign_roles='1';
    }else{
      $scope.assign_roles='';
    }
    if(roles.indexOf("Assign Dashboards") !== -1) {
      $scope.assign_dashboard='1';
    }else{
      $scope.assign_dashboard='';
    }
    if(roles.indexOf("Assign Countries") !== -1) {
      $scope.assign_countries='1';
    }else{
      $scope.assign_countries='';
    }
    if(roles.indexOf("Assign Hiearchies") !== -1) {
      $scope.assign_hiearchie='1';
    }else{
      $scope.assign_hiearchie='';
    }

  });
  $scope.popup_text='Add User';


  $scope.make_status=function(){
    if($('.user_id').val()!='')
    {
      if (confirm("Are you sure?"))
      {
        $('.ld').css({'display':'inline'}); $('.roll-msg').text('Please wait...');
        getUserService.userUpdate($('.user_id').val()).then(function(response){
          if(response.data.status=='success'){
            $scope.status='success';
            $scope.message='Record has been successfully updated';
            setTimeout(function() {
            $scope.status='';
            $scope.$apply();
          }, 3000);
          $('.ld').css({'display':'none'}); $('.roll-msg').text('Deactivate User');

          $('.table').find('.role-u').each(function(){
            if($(this).val()==$('.user_id').val()){
              $(this).prop( "checked", false );
              $('.user_id').val('');
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
      alert('Please choose any User.');
    }
  }

  $(document).on('click','.role-u',function(){
    $('.user_id').val($(this).val());
  });

  $scope.cmp={};

  $scope.close=function(){
    $scope.popup_text='Add User';
    $scope.edit_dat='';
  }
  $scope._add_user=function(){
    $scope.cmp={};
    $scope.edit_dat='1';
    $scope.popup_text='Add User';
  }

  $scope.userFormData=function(f){
      if($('.active_flag').is(":checked")){
        var stat='Y';
      }
      else{
        var stat='N';
      }

      var fd = new FormData();
      fd.append("company_id",$('.company_name').val());
      fd.append("password",$('.password').val());
      fd.append("user_name",$('.user_name').val());
      fd.append("fisrt_name",$('.fisrt_name').val());
      fd.append("nice_name",$('.nice_name').val());
      fd.append("last_name",$('.last_name').val());
      fd.append("email",$('.email').val());
      fd.append("active_flag",stat);
      fd.append("user_id",$('.edit_user_id').val());

      $('.lder').show(); $('.role_save').text('Please wait...');
      getUserService.userAdd(fd).then(function(response){
        if(response.data.status=='success'){
          $scope.userData=response.data.users;
          $scope.compData=response.data.compData;
          $scope.UserCompId=response.data.UserCompId;

          $scope.status_role='success';
          $scope.message_role='Record has been successfully Saved';
          $('.chk').val('');
          $('.role_active').prop( "checked", false );

          setTimeout(function() {
          $('.btn-default').trigger('click');
          $scope.status_role='';
          $scope.$apply();
        }, 3000);

      }else {
        $scope.status_role='danger';
        $scope.message_role='Sorry, This User is already exist in database';
        setTimeout(function() {
        $scope.status_role='';
        $scope.$apply();
      }, 5000);
      }
      $('.lder').hide(); $('.role_save').text('Save changes');
      });

  }

  $scope._assign_data_to_user=function(type){
    if($('.user_id').val()!='')
    {
      $('.AssignDataModel').trigger('click');
      $('.assign_type').val(type);
      $scope.popup_text='Assign '+type;
      $scope.user_companyName='';
      $scope.assign_type=type;
      var fd = new FormData();
      fd.append("user_id",$('.user_id').val());
      fd.append("assign_type",type);
      getUserService.userAssignData(fd).then(function(response){
          console.log(response);
        if(response.data.status=='success'){
            $scope.master_data=response.data.master_data;
            $scope.user_added_data=response.data.user_added_data;
            $scope.user_id=response.data.user_data[1];
            $scope.user_companyName=response.data.user_data[3];
            $scope.user_userName=response.data.user_data[1];
            $scope.user_emailAddress=response.data.user_data[2];
            $scope.user_company_id=response.data.user_data[4];
            setTimeout(function(){
              $('#optgroupEdit').multiselect();
            },1000);
        }

      });
    }
    else{
      alert('Please choose any User.');
    }
  }

  $scope.userRoleData=function(){
    $('.assign_data option').prop('selected', true);
    if($('.assign_data').val()!=null){

      var fd = new FormData();
      fd.append("user_id",$('._edit_user_id').val());
      fd.append("company_id",$('.edit_company_id').val());
      fd.append("assign_data",$('.assign_data').val());
      fd.append("assign_type",$('.assign_type').val());

      $('.lder').show(); $('.role_save').text('Please wait...');
      getUserService.userAssignDataAdd(fd).then(function(response){
        if(response.data.status=='success'){
          $scope.status_role='success';
          $scope.message_role='Record has been successfully Saved';
          $('.role-u').prop( "checked", false );
          $('.assign_data').empty(); $('.user_id').val('');
          setTimeout(function() {
          $('.btn-default').trigger('click');
          $scope.status_role='';
          $scope.$apply();
        }, 3000);

      }
      $('.lder').hide(); $('.role_save').text('Save changes');
     });
    }else{
      alert('Please select Role for User');
    }
  }

});
