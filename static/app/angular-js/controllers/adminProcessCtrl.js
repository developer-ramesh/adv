app.controller('adminProcessCtrl', function($window,$scope,$http,$routeParams,$location,getProcessService,$filter) {
  $scope.loading = true;
  getProcessService.getProcessData().then(function(response){
    $scope.loading = false;
    $scope.processdData=response.data.process;

    if(response.data.rolePermission.length==0){
      $window.location.href = '/#/not-permission';
    }else{
      if(jQuery.inArray("View Process", response.data.rolePermission) != -1) {
        //$scope.userRolePermission=response.data.rolePermission;
      } else {
        $window.location.href = '/#/not-permission';
      }
    }

    var roles=response.data.rolePermission;
    if(roles.indexOf("Add Process") !== -1) {
      $scope.add_process='1';
    }else{
      $scope.add_process='';
    }
    if(roles.indexOf("Update Process") !== -1) {
      $scope.update_process='1';
    }else{
      $scope.update_process='';
    }
    if(roles.indexOf("Deactivate Process") !== -1) {
      $scope.deactivate_process='1';
    }else{
      $scope.deactivate_process='';
    }

  });
  $scope.popup_text='Add Process';


  $scope.make_status=function(){
    if($('.process_id').val()!='')
    {
      if (confirm("Are you sure?"))
      {
        $('.ld').css({'display':'inline'}); $('.roll-msg').text('Please wait...');
        getProcessService.processUpdate($('.process_id').val()).then(function(response){
          console.log(response);
          if(response.data.status=='success'){
            $scope.status='success';
            $scope.message='Record has been successfully updated';
            setTimeout(function() {
            $scope.status='';
            $scope.$apply();
          }, 3000);
          $('.ld').css({'display':'none'}); $('.roll-msg').text('Deactivate Process');

          $('.table').find('.role-u').each(function(){
            if($(this).val()==$('.process_id').val()){
              $(this).prop( "checked", false );
              $('.process_id').val('');
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
      alert('Please choose any Process.');
    }
  }

  $(document).on('click','.role-u',function(){
    $('.process_id').val($(this).val());
  });
  $(document).on('click','#optgroupEdit_leftSelected, #optgroupEdit_rightSelected',function(){
    $('.assign_dashboard option').prop('selected', true);
  });

  $scope.close=function(){
    $scope.popup_text='Add Process';
    $scope.edit_role=''; $scope.assign_dashboard='';
    $scope.process_name='';
    $scope.long_name='';
    $scope.help_text='';
  }
  $scope._addProcess=function(){
    $scope.edit_role='';
    $scope.popup_text='Add Process';
    getProcessService.getProcessData().then(function(response){
      $scope.dataDashboard=response.data.dashboard;
      $scope.edit_role='11';
      $scope.process_image='';
      setTimeout(function(){
        $('#optgroupEdit').multiselect();
      },1000);
    });
  }

  $scope.processFormData=function(){
    $('.assign_dashboard option').prop('selected', true);
    if($('.assign_dashboard').val()!=null){
      if($('.role_active').is(":checked")){
        var stat='Y';
      }
      else{
        var stat='N';
      }

      var fd = new FormData();
      fd.append("process_name",$('.process_name').val());
      fd.append("long_name",$('.long_name').val());
      fd.append("help_text",$('.help_text').val());
      fd.append("process_active",stat);
      fd.append("assign_dashboard",$('.assign_dashboard').val());
      fd.append("process_id",$('.edit_process_id').val());
      fd.append("edit_pic_name",$('.edit_pic_name').val());
      fd.append("file",document.getElementById('pic').files[0]);

      $('.lder').show(); $('.role_save').text('Please wait...');
      getProcessService.processAdd(fd).then(function(response){
        if(response.data.status=='success'){
          $scope.processdData=response.data.process;
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
      alert('Please select Process for for Dashboard');
    }
  }


  $scope.editProcess=function(processID){
    $scope.edit_role='';
    $scope.popup_text='Edit Process';
    getProcessService.processEdit(processID).then(function(response){
      $scope.edit_role=response.data.process[0];
      $scope.dataDashboard=response.data.dashboardData;
      $scope.assigned_dashboard_data=response.data.user_added_dashboard;
      $scope.process_name=response.data.process[0].fields.short_name;
      $scope.long_name=response.data.process[0].fields.long_name;
      $scope.help_text=response.data.process[0].fields.description;
      $scope.process_image=response.data.process[0].fields.process_image;
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
