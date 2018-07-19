/**
 * Created by DAO on 2017/7/28.
 */

$(function () {
    $('select').change(function () {
        $('#select_form').submit();
    })
    // $('select').change(function () {
    //     val = $(this).val();
    //     $.ajax({
    //         url:'http://127.0.0.1:8085/app01/query/',
    //         dataType:JSON,
    //         type:'POST',
    //         data:{'select_class':val},
    //
    //         success:function (data) {
    //             console.log('成功');
    //             console.log(data);
    //         }
    //
    //     })
    // })
});