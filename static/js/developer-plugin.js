(function ( $ ) {

    $.fn.Jcount_data = function() {

      // this.each(function () {
      //   var ValueNum = $(this).attr('val');
      //   $(this).prop('Counter',0).animate({
      //     Counter:ValueNum
      //   }, {
      //     duration: 3000,
      //     easing: 'swing',
      //     step: function (now) {
      //       $(this).text(Math.ceil(now));
      //     }
      //   });
      // });
      //
      // return this;
    };




    $.fn.JchartByMonth=function(month_data,payment_month,currency_type,categories_data,expensestypelist,countries_data){
      //console.log(month_data);
      var amount = [];
      var month = [];
      $.each(month_data, function(key, value) {
          amount.push(value.amount);
          month.push(value.c_month_name);
      });

      line_chart_month=[];
      payment_average=[];
      $.each(payment_month, function(key, value) {
          nm=month_name(key[4]+''+key[5])+" '"+key[2]+''+key[3];
          line_chart_month.push(nm);
          //payment_average.push(arraySum(value)/value.length);
          payment_average.push(arraySum(value));
      });

      function arraySum(array_){
        var totalAmount = 0;
        for (var x = 0; x < array_.length; x++) {
          totalAmount += parseInt(array_[x]);
        }
        return totalAmount;
      }

      function month_name(_day){
        var day_name;
        if(_day=='01') {
          day_name = "Jan";
        }else if(_day=='02') {
          day_name = "Feb";
        }else if(_day=='03') {
          day_name = "Mar";
        }else if(_day=='04') {
          day_name = "Aprl";
        }else if(_day=='05') {
          day_name = "May";
        }else if(_day=='06') {
          day_name = "Jun";
        }else if(_day=='07') {
          day_name = "Jul";
        }else if(_day=='08') {
          day_name = "Aug";
        }else if(_day=='09') {
          day_name = "Sep";
        }else if(_day=='10') {
          day_name = "Oct";
        }else if(_day=='11') {
          day_name = "Nov";
        }else if(_day=='12') {
          day_name = "Dec";
        }
        return day_name;
      }

      function commaSeparateNumber(val){
         while (/(\d+)(\d{3})/.test(val.toString())){
           val = val.toString().replace(/(\d+)(\d{3})/, '$1'+','+'$2');
         }
         return val;
      }

      line_chart=[];
      $.each(month_data, function(key, value) {
          line_chart.push({'name':key,'data':value,'type':'column'});
      });

      line_chart.push({'type':'','name':'Total Spend','data':payment_average,'marker':{'lineWidth': 2,'fillColor':'white','lineColor':Highcharts.getOptions().colors[3]} });

      var category_list = [];
      var expense_list = [];
      $.each(categories_data, function(key, value) {
          category_list.push({name:value.spend_category_name , value:value.amount, colorValue:value.amount });
      });

      var expense_list = [];
      $.each(expensestypelist, function(key, value) {
          expense_list.push({name:value.expense_type_name , value:value.amount, colorValue:value.amount });
      });

      /*** BY - Month*************************************************/

      Highcharts.setOptions({ lang: { thousandsSep: ',' }});

      $('#by-month').highcharts({
        title: {
            text: ''
        },
        credits: {
            enabled: false
        },
        tooltip: {
            valuePrefix: currency_type
        },
        yAxis: {
              // min: 0,
              title: {
                  text: ''
              }
              //categories: payment_sum
        },
        xAxis: {
            categories: line_chart_month
        },
        labels: {
            items: [{
                html: '',
                style: {
                    left: '50px',
                    top: '18px',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'black'
                }
            }]
        },
        series: line_chart
      });

      //   $('#by-month').highcharts({
      //   chart: {
      //       type: 'column'
      //   },
      //   credits: {
      //     enabled: false
      //   },
      //   title: {
      //       text: ''
      //   },
      //   xAxis: {
      //       categories: amount
      //   },
      //   yAxis: {
      //       min: 0,
      //       title: {
      //           text: ''
      //       }
      //   },
      //   tooltip: {
      //       pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
      //       shared: true
      //   },
      //   plotOptions: {
      //       column: {
      //           stacking: 'percent'
      //       }
      //   },
      //   //series: [ { name: 'John', data: [5, 3, 4, 7, 2] }, { name: 'Jane', data: [2, 2, 3, 2, 1] }]
      //   series: line_chart
      // });


      // $('#by-month').highcharts({
      //       title: {
      //           text: '',
      //       },
      //       xAxis: {
      //           categories: month
      //       },
      //       yAxis: {
      //           title: {
      //               text: ''
      //           },
      //           plotLines: [{
      //               value: 0,
      //               width: 1,
      //               color: '#808080'
      //           }]
      //       },
    	// 	credits: {
    	// 		enabled: false
    	// 	},
      //       tooltip: {
      //           valuePrefix: currency_type
      //       },
      //       legend: {
      //           layout: 'vertical',
      //           align: 'right',
      //           verticalAlign: 'middle',
      //           borderWidth: 0
      //       },
      //       series: [{
    	// 		showInLegend: false,
      //           name: 'month',
      //           data: amount
      //       }]
      //   });
        /*** End bY - Month*************************************************/


        /*** BY - Category*************************************************/

        Highcharts.seriesTypes.treemap.prototype.pointArrayMap.push('node.val');

        $('#tree-map').highcharts({
          colorAxis: {
          minColor: '#FFFFFF',
          maxColor: Highcharts.getOptions().colors[0]
        },
        legend:{
          //enabled: false
        },
          series: [{
            type: 'treemap',
            layoutAlgorithm: 'squarified',
            data: category_list
          }],
          title: {
            text: ''
          },
          credits: {
            enabled: false
          },
          tooltip: {
              valuePrefix: currency_type
          }
        });

        $('#tree-map2').highcharts({
  				colorAxis: {
  				minColor: '#FFFFFF',
  				maxColor: Highcharts.getOptions().colors[0]
  			},legend:{
          //enabled: false
        },
  				series: [{
  					type: 'treemap',
  					layoutAlgorithm: 'squarified',
  					data: expense_list
  				}],
  				title: {
  					text: ''
  				},
          tooltip: {
              valuePrefix: currency_type
          },
  				credits: {
  					enabled: false
  				}
  			});
        /*** End by category*************************************************/


        /*** Start By Country*************************************************/
        var geocoder = new google.maps.Geocoder();
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 1,
          mapTypeControl: false,
          streetViewControl: false,
          disableDefaultUI: false,
          mapTypeId: google.maps.MapTypeId.ROADMAP,
          scrollwheel: false
          //center: {lat: -33, lng: 151}
        });

        map.set('styles', [
          {
           featureType: "landscape",
           featureType: "natural",
           eatureType: "water",
           elementType: "geometry",
           stylers: [
             { hue: "#cccccc" },
             { saturation: -50000 },
             { lightness: -5 }
           ]
         } ,
      {
        featureType: "water",
        elementType: "geometry",
        stylers: [
            { invert_lightness: true },
            { hue: "#ff003b" },
            { saturation: 50 },
            { lightness: 100 }
        ]
      }
      ]);

        function geocodeAddress(geocoder, resultsMap , address , bubbleSize , amt) {
          geocoder.geocode({'address': address}, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
              resultsMap.setCenter(results[0].geometry.location);
              var marker = new MarkerWithLabel({
                map: resultsMap,
                position: results[0].geometry.location,
                labelAnchor: new google.maps.Point(10, 10),
                labelClass: "pointer",
                labelContent: '<div class="address" data-address="'+address+'" data-size="'+bubbleSize+'"></div>',
                labelStyle: {opacity: 0.75},
                icon: {
                   path: google.maps.SymbolPath.CIRCLE,
                   scale: 0, //tamaño 0
                }
              });

              var infowindow = new google.maps.InfoWindow({});
              google.maps.event.addListener(marker, 'click', function() {
                  infowindow.setContent(address+': '+currency_type+commaSeparateNumber(amt));
                  infowindow.open(resultsMap, marker);
              });

            } else {
              console.log('Geocode was not successful for the following reason: ' + status);
            }
          });
        }

        var countries = []; var country_amount =[];
        $.each(countries_data, function(key, value) {
            country_amount.push(value.amount);
        });
        country_amount=Math.max.apply(Math, country_amount);

        $.each(countries_data, function(key, value) {
            pxsize=Math.round(value.amount/country_amount*50);
            geocodeAddress(geocoder, map , value.location_country, pxsize,value.amount);
        });




        google.maps.event.addListener(map, 'idle', function() {
          $('body').find('.address').each(function(){
            widHt=$(this).data('size');
            if(widHt>=300){
                widHt=Math.round(widHt/99);
                HalfSiz=Math.round(widHt/100);
            }else{
              HalfSiz=Math.round(widHt/2);
            }
            $(this).css("cssText", "width:"+widHt+"px !important;height:"+widHt+"px !important;margin-left:-"+HalfSiz+"px;margin-top:-"+HalfSiz+"px;");
          });
        });
        /*** End By Country*************************************************/

        setTimeout(function(){
          $('body').find('.address').each(function(){
            widHt=$(this).data('size');
            if(widHt>=300){
                widHt=Math.round(widHt/99);
                HalfSiz=Math.round(widHt/100);
            }else{
              HalfSiz=Math.round(widHt/2);
            }
            $(this).css("cssText", "width:"+widHt+"px !important;height:"+widHt+"px !important;margin-left:-"+HalfSiz+"px;margin-top:-"+HalfSiz+"px;");
          });



          $('[data-toggle="tooltip"]').tooltip();
    			$('body').on('click','*', function () { $(this).tooltip('hide'); });

          var date = new Date();
          var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    			$('#StartTime').datetimepicker({
    				format: 'YYYY-MM-DD',
            maxDate: today
    			});
    			$('#EndTime').datetimepicker({
    				format: 'YYYY-MM-DD',
            maxDate: today,
    				useCurrent: false //Important! See issue #1075
    			});
    			$('#StartTime').on('dp.change', function (e) {
    				$('#EndTime').data('DateTimePicker').minDate(e.date);
    			});
    			$('#EndTime').on('dp.change', function (e) {
    				$('#StartTime').data('DateTimePicker').maxDate(e.date);
    			});



        },1000);


    }

}( jQuery ));
