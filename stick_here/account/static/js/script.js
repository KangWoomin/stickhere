$(document).ready(function(){
    $('.toggle').on('click', function(){
        $('.sidebar').toggleClass('show');
    });

    $('.dropdown-toggle').on('click', function(){
        $(this).next('.dropdown-menu').slideToggle(500);
    });
});
