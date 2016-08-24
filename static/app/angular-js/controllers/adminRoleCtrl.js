app.controller('adminRoleCtrl', function($window,$scope,$http,$routeParams,$location,getRoleService,$filter) {
  $scope.loading = true;
  getRoleService.getRolesData().then(function(response){
    $scope.loading = false;
    $scope.roleData=response.data.dataRole;
    $scope.permissionData=response.data.permission;

    if(response.data.rolePermission.length==0){
      $window.location.href = '/#/not-permission';
    }else{
      if(jQuery.inArray("View Role", response.data.rolePermission) != -1) {
        //$scope.userRolePermission=response.data.rolePermission;
      } else {
        $window.location.href = '/#/not-permission';
      }
    }

    var roles=response.data.rolePermission;
    if(roles.indexOf('Add Role') !== -1) {
      $scope.addrole='1';
    }else{
      $scope.addrole='';
    }
    if(roles.indexOf('Update Role') !== -1) {
      $scope.update_role='1';
    }else{
      $scope.update_role='';
    }
    if(roles.indexOf('Deactivate Role') !== -1) {
      $scope.deactivate_role='1';
    }else{
      $scope.deactivate_role='';
    }
    if(roles.indexOf('Manage Restricted Role') !== -1) {
      $scope.manage_restricted_role='1';
    }else{
      $scope.manage_restricted_role='';
    }


  });
  $scope.popup_text='Add Role';


  $scope.make_status=function(){
    if($('.role_id').val()!='')
    {
      if (confirm("Are you sure?"))
      {
        $('.ld').css({'display':'inline'}); $('.roll-msg').text('Please wait...');
        getRoleService.roleUpdate($('.role_id').val()).then(function(response){
          console.log(response);
          if(response.data.status=='success'){
            $scope.status='success';
            $scope.message='Record has been successfully updated';
            setTimeout(function() {
            $scope.status='';
            $scope.$apply();
          }, 3000);
          $('.ld').css({'display':'none'}); $('.roll-msg').text('Deactivate Role');

          var currentTime = new Date();

          $('.table').find('.role-u').each(function(){
            if($(this).val()==$('.role_id').val()){
              $(this).prop( "checked", false );
              $('.role_id').val('');
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
      alert('Please choose any Role.');
    }
  }

  $(document).on('click','.role-u',function(){
    $('.role_id').val($(this).val());
  });
  $(document).on('click','#optgroupEdit_leftSelected, #optgroupEdit_rightSelected',function(){
    $('.assign_permission option').prop('selected', true);
  });
  $(document).on('click','.btn-default , .close',function(){
    //$('.chk').val('');$('.role_active , .role_restricted').prop( "checked", false );$('.assign_permission').empty();
  });
  $scope.close=function(){
    $scope.popup_text='Add Role';
    $scope.edit_role=''; $scope.asign_permission='';
    $scope.role_name='';
    $scope.role_description='';
  }
  $scope.add_role=function(){
    $scope.edit_role='';
    $scope.popup_text='Add Role';
    getRoleService.getRolesData().then(function(response){
      $scope.permissionData=response.data.permission;

      var roles=response.data.rolePermission;
      if(roles.indexOf('Manage Restricted Role') !== -1) {
        $scope.manage_restricted_role='1';
      }else{
        $scope.manage_restricted_role='';
      }

      $scope.edit_role='11';
      setTimeout(function(){
    		$('#optgroupEdit').multiselect();
    	},1000);
    });

  }

  $scope.roleFormData=function(){
    if($('.assign_permission').val()!=null){
      $('.assign_permission option').prop('selected', true);
      $('.lder').show(); $('.role_save').text('Please wait...');
      getRoleService.roleAdd($('.frm').serialize()).then(function(response){
        if(response.data.status=='success'){
          $scope.roleData=response.data.dataRole;
          $scope.status_role='success';
          $scope.message_role='Record has been successfully Saved';
          $('.chk').val('');
          $('.role_active , .role_restricted').prop( "checked", false );
          $('.assign_permission').empty();
          setTimeout(function() {
          $('.btn-default').trigger('click');
          $scope.status_role='';
          $scope.$apply();
        }, 3000);

      }else {
        $scope.status_role='danger';
        $scope.message_role='Sorry, This role is already exist in database';
        setTimeout(function() {
        $scope.status_role='';
        $scope.$apply();
      }, 5000);
      }
      $('.lder').hide(); $('.role_save').text('Save changes');
      });
    }else{
      alert('Please select permissions for Role');
    }
  }


  $scope.editRole=function(roleId){
    $scope.edit_role='';
    $scope.popup_text='Edit Role';
    getRoleService.roleEdit(roleId).then(function(response){
      $scope.edit_role=response.data.role[0];
      $scope.permissionData=response.data.permissions;
      $scope.asign_permission=response.data.user_permission;
      $scope.role_name=response.data.role[0].fields.role_name;
      $scope.role_description=response.data.role[0].fields.description;

      var roles=response.data.rolePermission;
      if(roles.indexOf('Manage Restricted Role') !== -1) {
        $scope.manage_restricted_role='1';
      }else{
        $scope.manage_restricted_role='';
      }

      setTimeout(function(){
    		$('#optgroupEdit').multiselect();
        $('.assign_permission option').prop('selected', true);
    	},1000);
    });
  }

});
