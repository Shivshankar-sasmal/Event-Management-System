$(document).ready(function(){
        $('.acc h4').click(function(){
            $(this).next('.content').slideToggle();
            $(this).parent().toggleClass('active');
            $(this).parent().siblings().children('.content').slideUp();
            $(this).parent().siblings().removeClass('active');
        });

        $('.event_content_touch .blog-header img').click(function(){
            $(this).parent().next('.content_event').slideToggle();
            $(this).parent().parent().siblings().children('.content_event').slideUp();
        });

        minDate = new Date();
        $("#id_event_date").datepicker({
            showAnim : 'drop',
            numberOfMonth : 1,
            minDate : minDate,
        });
});

