$(document).ready(function(){
    $('select[name=province]').change(function(){
            province_id = $(this).val();
            // console.log(province_id);
            request_url = '/bdiadmin/get_commune/' + province_id + '/';
            $.ajax({
                url: request_url,
                dataType: "json",
                success: function(data){
                    $('select[name=commune]').val(''); // remove the value from the input
                    // console.log(data);
                    data = $.parseJSON(data);
                    // console.log(data); // log the returned json to the console
                    $.each(data, function(key, value){
                         // $('select[name=commune]').val('');
                         for (var i in value) {
                            // console.log(i);
                            $('select[name=commune]').append('<option value="' + i+ '">' + value[i] +'</option>');
                         }
                    });
                },
            });
            return false; //<---- move it here
        });
    $('select[name=commune]').change(function(){
            commune_id = $(this).val();
            console.log(commune_id);
            request_url = '/bdiadmin/get_colline/' + commune_id + '/';
            $.ajax({
                url: request_url,
                dataType: "json",
                success: function(data){
                    $('select[name=colline]').val(''); // remove the value from the input
                    // console.log(data);
                    data = $.parseJSON(data);
                    // console.log(data); // log the returned json to the console
                    $.each(data, function(key, value){
                         // $('select[name=colline]').val('');
                         for (var i in value) {
                            // console.log(i);
                            $('select[name=colline]').append('<option value="' + i+ '">' + value[i] +'</option>');
                         }
                    });
                },
            });
            return false; //<---- move it here
        });
});