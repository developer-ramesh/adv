app.controller('adminMessageCtrl', function($window,$scope,$http,$routeParams,$location,getMessageService,$filter) {
  $scope.loading = true;
  getMessageService.getMessageData().then(function(response){
    $scope.loading = false;
    $scope.messageData=response.data.messages;
    $scope.compData=response.data.compData;
    $scope.UserCompId=response.data.UserCompId;
    if(response.data.rolePermission.length==0){
      $window.location.href = '/#/not-permission';
    }else{
      if(jQuery.inArray("View Message", response.data.rolePermission) != -1) {
      } else {
        $window.location.href = '/#/not-permission';
      }
    }


    var roles=response.data.rolePermission;
    if(roles.indexOf("Add Company Message") !== -1) {
      $scope.add_company_message='1';
    }else{
      $scope.add_company_message='';
    }
    if(roles.indexOf("Add System Message") !== -1) {
      $scope.add_system_message='1';
    }else{
      $scope.add_system_message='';
    }
    if(roles.indexOf("Update Company Message") !== -1) {
      $scope.update_company_message='1';
    }else{
      $scope.update_company_message='';
    }
    if(roles.indexOf("Update System Message") !== -1) {
      $scope.update_system_message='1';
    }else{
      $scope.update_system_message='';
    }
    if(roles.indexOf("Deactivate Message") !== -1) {
      $scope.deactivate_message='1';
    }else{
      $scope.deactivate_message='';
    }

  });
  $scope.popup_text='Add Message';


  $scope.make_status=function(){
    if($('.message_id').val()!='')
    {
      if (confirm("Are you sure?"))
      {
        $('.ld').css({'display':'inline'}); $('.roll-msg').text('Please wait...');
        getMessageService.messageUpdate($('.message_id').val()).then(function(response){
          if(response.data.status=='success'){
            $scope.status='success';
            $scope.message='Record has been successfully updated';
            setTimeout(function() {
            $scope.status='';
            $scope.$apply();
          }, 3000);
          $('.ld').css({'display':'none'}); $('.roll-msg').text('Deactivate Message');

          $('.table').find('.role-u').each(function(){
            if($(this).val()==$('.message_id').val()){
              $(this).prop( "checked", false );
              $('.message_id').val('');
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
      alert('Please choose any Message.');
    }
  }

  $(document).on('click','.role-u',function(){
    $('.message_id').val($(this).val());
  });

  $scope.cmp={};

  $scope.close=function(){
    $scope.popup_text='Add Message';
    $scope.edit_dat='';
  }
  $scope._add_company_message=function(){
    $scope.cmp={};
    $scope.edit_dat='1';

    setTimeout(function() {
      $scope.popup_text='Add Message';
      $scope.$apply();
    }, 1000);

    $('.message_type').val('C');
  }
  $scope._add_system_message=function(){
    $scope.cmp={};
    $scope.edit_dat='1';
    $('.message_type').val('S');

    setTimeout(function() {
      $scope.popup_text='Add System Message';
      $scope.$apply();
    }, 1000);
  }

  $scope.messageFormData=function(f){
      if($('.active_flag').is(":checked")){
        var stat='Y';
      }
      else{
        var stat='N';
      }

      var fd = new FormData();
      fd.append("company_name",$('.company_name').val());
      fd.append("message_text",$('.message_text').val());
      fd.append("active_flag",stat);
      fd.append("message_type",$('.message_type').val());
      fd.append("message_id",$('.edit_message_id').val());

      $('.lder').show(); $('.role_save').text('Please wait...');
      getMessageService.messagedAdd(fd).then(function(response){
        if(response.data.status=='success'){
          $scope.messageData=response.data.messages;
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
        $scope.message_role='Sorry, This Message is already exist in database';
        setTimeout(function() {
        $scope.status_role='';
        $scope.$apply();
      }, 5000);
      }
      $('.lder').hide(); $('.role_save').text('Save changes');
      });

  }


  $scope.editMessage=function(messageID){
    $scope.cmp.edit_dat='';
    $scope.popup_text='Edit Message';
    getMessageService.messageEdit(messageID).then(function(response){
      $scope.cmp.edit_dat=response.data.message[0];
      $scope.cmp.message_text=response.data.message[0].fields.message_text;
    });
  }


  $scope.lnc_update=function(cpid){
    var fd = new FormData();
    fd.append("comp_process_id",cpid);
    fd.append("license",$('#licence_'+cpid).val());
    getCompanyService.companyLicenseUpdate(fd).then(function(response){
      if(response.data.status=='danger'){
        $scope.status_role='danger';
        $scope.message_role='Sorry, This License is already exist in database';
        setTimeout(function() {
        $scope.status_role='';
        $scope.$apply();
      }, 4000);
      }
    });
  }

});
