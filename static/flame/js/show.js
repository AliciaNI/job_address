/**
 * Created by DAO on 2017/9/15.
 */
$(document).ready(function () {
    $('table').parent().attr('style', 'margin-left: 0%;width: 100%;');
    var add_page_func_flags = 0;   // 作为以哪种方式添加页码的标志，等于0从1开始加，大于0添加新的页码。
    var old_data_nums = 0;         // 保存上一次的数据量，作为是否添加新页的标志
    var i = 0;                     // 页码号
    var pagenums = 0;   // 有多少页
    var everynums = Math.floor($('#everynums').val()); // 每页有多少条
    console.log('zzz2346558795654zzz', everynums);
    var prepagenum = 1;  // 记录上一次点击的页码数
    $('tr').slice(1, everynums+1).removeAttr('style');
    setInterval(function () {
        // 加载数据
        $.ajax({
            url: "/flame/tourldata/",
            type: "POST",
            success: function (datalistb) {
                // console.log('a', datalistb.length);
                if (datalistb.length > 0) {
                    // console.log('b', datalistb.length);
                    $(datalistb).each(function (index, element) {
                        // console.log('c', index, element);
                        $('<tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>').appendTo($('table'));
                        $('tr:last>td:eq(0)').text(element.company);
                        $('<ul><li>' + element.company + '</li></ul>').appendTo($('tr:last>td:eq(0)'));
                        $('tr:last>td:eq(1)').text(element.job);
                        $('<ul><li>' + element.job + '</li></ul>').appendTo($('tr:last>td:eq(1)'));
                        $('tr:last>td:eq(2)').text(element.salary);
                        $('tr:last>td:eq(3)').text(element.job_infor);
                        $('<ul><li>' + element.job_infor + '</li></ul>').appendTo($('tr:last>td:eq(3)'));
                        $('tr:last>td:eq(4)').text(element.company_infor);
                        $('<ul><li>' + element.company_infor + '</li></ul>').appendTo($('tr:last>td:eq(4)'));
                        $('<a>' + element.address + '</a>').appendTo($('tr:last>td:eq(5)'));
                        $('<ul><li>' + element.address + '</li></ul>').appendTo($('tr:last>td:eq(5)'));
                        var abiaoqian = $('tr:last>td:eq(5)>a');
                        abiaoqian.attr('href', "/flame/map?lng=" + element.lng + "&lat=" + element.lat);
                        abiaoqian.attr('target', "_blank");
                        // 并且tr数量大于everynums,
                        console.log('在同辈中的索引', $('tr:last').index(), $('tr').index($('tr:last')));
                        if ($('tr:last').index() > everynums) {
                            $('tr:last').attr('style', 'display: none;');
                        }
                    })
                }
            }
        });

        // 算页码

        // 获取tr标签
        // 每页20条， 计算共多少页
        // 显示页码
        // 显示第一页
        var trlist = $('tr');  // 获取所有tr标签

        var datalen = trlist.length;  // tr标签的长度，即数据量
        console.log('datalen', datalen, datalen % everynums);
        // 计算页码
        if (datalen % everynums == 0) {
            pagenums = Math.floor(datalen / everynums)
        }
        else {
            pagenums = Math.floor(datalen / everynums) + 1
        }
        // console.log('pagenums', pagenums);

        // 加页码
        // 如果已有页码，那么只有当有新数据需要新页时再添加
        if (add_page_func_flags == 0) {
            for (i = 1; i <= pagenums; i++) {
                // console.log('i', i);
                $('<li><a href="#">' + i + '</a></li>').insertAfter($('.pagination>li:eq(-2)'));
                // console.log($('.pagination>li'));
                // 给页码加点击事件， li标签的倒数第二个
                $('.pagination>li:eq(-2)').find('a').click(function () {
                    // 显示对应页码的数据
                    // console.log('看我72变。');
                    var pagenum = Math.floor($(this).text());
                    // console.log('页码', pagenum, typeof pagenum);
                    var qi = (pagenum - 1) * everynums+1;
                    var zhong = pagenum * everynums + 1;
                    // console.log('起始终止', qi, zhong);
                    // 隐藏上一次点击页码的数据，
                    $('tr').slice((prepagenum-1)*everynums+1, prepagenum*everynums+1).attr('style', 'display: none;');
                    // 显示这一次点击页码的数据
                    $('tr').slice(qi, zhong).removeAttr('style');
                    // 保存点击的页码
                    prepagenum = pagenum
                })
            }
        }
        else {
            if (pagenums >= i) {
                for (i; i <= pagenums; i++) {
                    $('<li><a href="#">' + i + '</a></li>').insertAfter($('.pagination>li:eq(-2)'))
                    // console.log($('.pagination>li'));
                    // 给页码加点击事件， li标签的第二个到倒数第二个
                    $('.pagination>li:eq(-2)').find('a').click(function () {
                        // 显示对应页码的数据
                        // console.log('看我72变。');
                        var pagenum = Math.floor($(this).text());
                        // console.log('页码', pagenum, typeof pagenum);
                        var qi = (pagenum - 1) * everynums+1;
                        var zhong = pagenum * everynums+1;
                        // console.log('起始终止', qi, zhong);
                        // 隐藏上一次点击页码的数据，
                        // console.log($('tr').length, datalen);  // datalen的值变了， 不知为什么，但不报错
                        $('tr').slice((prepagenum-1)*everynums+1, prepagenum*everynums+1).attr('style', 'display: none;');
                        // 显示这一次点击页码的数据
                        $('tr').slice(qi, zhong).removeAttr('style');
                        // 保存点击的页码
                        prepagenum = pagenum
                    })
                }
            }
        }
        // 以哪种方式加页码的标志加1
        add_page_func_flags = add_page_func_flags + 1;

    }, 2000);
});