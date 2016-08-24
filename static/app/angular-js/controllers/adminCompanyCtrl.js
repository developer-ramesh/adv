app.controller('adminCompanyCtrl', function($window,$scope,$http,$routeParams,$location,getCompanyService,$filter) {
  $scope.loading = true;
  getCompanyService.getCompanyData().then(function(response){
    $scope.loading = false;
    $scope.companyData=response.data.company;

    if(response.data.rolePermission.length==0){
      $window.location.href = '/#/not-permission';
    }else{
      if(jQuery.inArray("View Company", response.data.rolePermission) != -1) {
      } else {
        $window.location.href = '/#/not-permission';
      }
    }


    var roles=response.data.rolePermission;
    if(roles.indexOf("Add Company") !== -1) {
      $scope.add_company='1';
    }else{
      $scope.add_company='';
    }
    if(roles.indexOf("Update Company") !== -1) {
      $scope.update_company='1';
    }else{
      $scope.update_company='';
    }
    if(roles.indexOf("Deactivate Company") !== -1) {
      $scope.deactivate_company='1';
    }else{
      $scope.deactivate_company='';
    }
    if(roles.indexOf("Manage Licenses") !== -1) {
      $scope.manage_license='1';
    }else{
      $scope.manage_license='';
    }
    if(roles.indexOf("Manage Dashboards") !== -1) {
      $scope.manage_dashboard='1';
    }else{
      $scope.manage_dashboard='';
    }

  });
  $scope.popup_text='Add Company';


  $scope.make_status=function(){
    if($('.company_id').val()!='')
    {
      if (confirm("Are you sure?"))
      {
        $('.ld').css({'display':'inline'}); $('.roll-msg').text('Please wait...');
        getCompanyService.companyUpdate($('.company_id').val()).then(function(response){
          if(response.data.status=='success'){
            $scope.status='success';
            $scope.message='Record has been successfully updated';
            setTimeout(function() {
            $scope.status='';
            $scope.$apply();
          }, 3000);
          $('.ld').css({'display':'none'}); $('.roll-msg').text('Deactivate Company');

          $('.table').find('.role-u').each(function(){
            if($(this).val()==$('.company_id').val()){
              $(this).prop( "checked", false );
              $('.company_id').val('');
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
      alert('Please choose any Company.');
    }
  }

  $(document).on('click','.role-u',function(){
    $('.company_id').val($(this).val());
  });

  $scope.cmp={};

  $scope.close=function(){
    $scope.popup_text='Add Company';
    $scope.edit_dat='';
  }
  $scope._add_company=function(){
    $scope.cmp={};
    $scope.cmp.logo='';
    $scope.edit_dat='1';
    $scope.popup_text='Add Company';
  }

  $scope.companyFormData=function(f){

      if($('.active_flag').is(":checked")){
        var stat='Y';
      }
      else{
        var stat='N';
      }
      if($('.single_sign_on_flag').is(":checked")){
        var single_stat='Y';
      }
      else{
        var single_stat='N';
      }

      var fd = new FormData();
      fd.append("short_name",$('.short_name').val());
      fd.append("full_name",$('.full_name').val());
      fd.append("address1",$('.address1').val());
      fd.append("address2",$('.address2').val());
      fd.append("city",$('.city').val());
      fd.append("state",$('.state').val());
      fd.append("country",$('.country').val());
      fd.append("zip_code",$('.zip_code').val());
      fd.append("primary_contact_name",$('.primary_contact_name').val());
      fd.append("primary_contact_email",$('.primary_contact_email').val());
      fd.append("primary_contact_phone",$('.primary_contact_phone').val());
      fd.append("secondary_contact_name",$('.secondary_contact_name').val());
      fd.append("secondary_contact_email",$('.secondary_contact_email').val());
      fd.append("secondary_contact_phone",$('.secondary_contact_phone').val());
      fd.append("landing_page_text",$('.landing_page').val());
      fd.append("single_sign_on_flag",single_stat);
      fd.append("active_flag",stat);
      fd.append("company_id",$('.edit_company_id').val());
      fd.append("edit_pic_name",$('.edit_pic_name').val());
      fd.append("file",document.getElementById('pic').files[0]);

      $('.lder').show(); $('.role_save').text('Please wait...');
      getCompanyService.companyAdd(fd).then(function(response){
        //console.log(response);
        if(response.data.status=='success'){
          $scope.companyData=response.data.company;
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
        $scope.message_role='Sorry, This Company is already exist in database';
        setTimeout(function() {
        $scope.status_role='';
        $scope.$apply();
      }, 5000);
      }
      $('.lder').hide(); $('.role_save').text('Save changes');
      });

  }


  $scope.editCompany=function(companyID){
    $scope.cmp.edit_dat='';
    $scope.popup_text='Edit Company';
    getCompanyService.companyEdit(companyID).then(function(response){
      $scope.cmp.edit_dat=response.data.company[0];
      $scope.cmp.short_name=response.data.company[0].fields.short_name;
      $scope.cmp.full_name=response.data.company[0].fields.full_name;
      $scope.cmp.address1=response.data.company[0].fields.address1;
      $scope.cmp.address2=response.data.company[0].fields.address2;
      $scope.cmp.city=response.data.company[0].fields.city;
      $scope.cmp.state=response.data.company[0].fields.state;
      $scope.cmp.country=response.data.company[0].fields.country;
      $scope.cmp.zip_code=response.data.company[0].fields.zip_code;
      $scope.cmp.primary_contact_name=response.data.company[0].fields.primary_contact_name;
      $scope.cmp.primary_contact_email=response.data.company[0].fields.primary_contact_email;
      $scope.cmp.primary_contact_phone=response.data.company[0].fields.primary_contact_phone;
      $scope.cmp.secondary_contact_name=response.data.company[0].fields.secondary_contact_name;
      $scope.cmp.secondary_contact_email=response.data.company[0].fields.secondary_contact_email;
      $scope.cmp.secondary_contact_phone=response.data.company[0].fields.secondary_contact_phone;
      $scope.cmp.landing_page_text=response.data.company[0].fields.landing_page_text;
      $scope.cmp.logo=response.data.company[0].fields.logo;
      console.log($scope.cmp.logo);
      setTimeout(function(){
    		$('#optgroupEdit').multiselect();
    	},1000);
    });
  }

  $scope._manage_license=function(){
    if($('.company_id').val()!='')
    {
      $('.manage_license').trigger('click');
      $scope.compnay_licenses=''; $scope.comp_name=''
      $scope.popup_text='Manage Licenses';
      getCompanyService.companyLicense($('.company_id').val()).then(function(response){
        $scope.comp_name=response.data.company_data[0].short_name;
        $scope.comp_fullname=response.data.company_data[0].full_name;
        $scope.compnay_licenses=response.data.compnay_licenses;
      });
    }
    else{
      alert('Please choose any Company.');
    }
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

  $scope.license_close=function(){
      $scope.status='success';
      $scope.message='Record has been successfully Saved';
      setTimeout(function() {
      $('.btn-default').trigger('click');
      $scope.status='';
      $scope.$apply();
    }, 3000);
  }

  $scope._manage_dashboard=function()
  {
    if($('.company_id').val()!='')
    {
      $('.manage_dashboard').trigger('click');
      $scope.popup_text='Manage Dashboards'; $scope.dash_company_name='';
      getCompanyService.companyDashboards($('.company_id').val()).then(function(response){
        $scope.dash_company_name=response.data.company_data[0].short_name;
        $scope.dash_company_full_name=response.data.company_data[0].full_name;
        $scope.asigned_dashboard=response.data.asigned_dashboard;
        $scope.available_dashboards=response.data.available_dashboards;
        setTimeout(function(){
      		$('#optgroup').multiselect();
      	},1000);
      });
    }
    else{
      alert('Please choose any Company.');
    }
  }

  $scope.dashboardFormData=function()
  {
    $('.assign_dashboard option').prop('selected', true);
    if($('.assign_dashboard').val()!=null)
    {
      var fd = new FormData();
      fd.append("company_id",$('.company_id').val());
      fd.append("assigned_dashboard",$('.assign_dashboard').val());

      $('.lder').show(); $('.role_save').text('Please wait...');
      getCompanyService.companyDashboardsUpdate(fd).then(function(response){
        $scope.status_role='success';
        $scope.message_role='Record has been successfully Saved';
        setTimeout(function() {
        $('.btn-default').trigger('click');
        $scope.status_role='';
        $scope.$apply();
        }, 3000);

        $('.lder').hide(); $('.role_save').text('Manage Dashboards');
      });

    }
    else{
      alert('Please select Dashboard for Company');
    }
  }

  $(document).on('change','#pic',function(event)
  {
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
