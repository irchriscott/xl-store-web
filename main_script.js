/**
	Main Scripts for xl-Store
	Date: Saturday, 19th May 2017
	Author: Ir Christian Scott
**/

var edit_cover = false;
var edit_profile = false;
var markers = [];
var map;

var host = 'localhost';
var port = '4000';
var socket = io(host + ':' + port);

$(function(){

    //Search Modal

    $("#open-search-modal").click(function(){
        $("#xl-search-modal").fadeIn();
        $(".xl-navbar-right").fadeOut();
        $(".xl-navbar-left").fadeOut();
        var address = $("#gen_address").val();
        if(address == ""){getUserCurrentLocation("gen_lat", "gen_lon", "gen_address");}
    });

    $("#close-searh-modal").click(function(){
        $("#xl-search-modal").fadeOut();
        $(".xl-navbar-right").fadeIn();
        $(".xl-navbar-left").fadeIn();
    });

    //Category Model

    $('#open_edit_category, #open_send_location, #open_upload_others_else').magnificPopup({
        type: 'inline',
        fixedContentPos: false,
        fixedBgPos: true,
        overflowY: 'auto',
        closeBtnInside: true,
        preloader: false,
        midClick: true,
        removalDelay: 300,
        mainClass: 'my-mfp-zoom-in'
    });

    $("#open_add_category, #open_edit_category, #load_address_map, #load_follow_categories, #load_user_carts_and_bills").magnificPopup({type:'ajax'});

    $("#close_add_category, #close_edit_category, #close_send_location, #close_upload_others").click(function(){
        $(".mfp-close").click();
    });

    $("#open_send_location").click(function(){
        initMapUser();
    });

    //Show and Hide nav

    $("#show-hide-nav").click(function(e){
        e.stopPropagation();
        $("#xl-leftnav").addClass('open');
    });

    $("#see_menu").showMenu();

    $("#show-user-options").click(function(ev){
        ev.stopPropagation();
        $("#xl-navbar-user-options").fadeIn();
        $(this).parent('li').removeClass('picture-header');
    });

    $("#open-logout-menu").click(function(ev){
        ev.stopPropagation();
        $("#xl-ms-logout-menu").fadeIn()
    });

    $("#open_send_others").showMenu();

    $("#open_change_status").showMenu();

    $(window).click(function(e){
        if($("#xl-leftnav").hasClass('open')){
            $("#xl-leftnav").removeClass('open');
        }
        $("#xl-navbar-user-options").fadeOut();
        $("#show-user-options").parent('li').addClass('picture-header');
        $("#xl-add-product-menu").fadeOut();
        $("#xl-ms-logout-menu").fadeOut();
        $(".xl-ms-product-menu").hide();
        $(".xl-ms-product-menu-else").hide();
    });

    $("#xl-leftnav").click(function(ev){
        ev.stopPropagation();
    });

    $("#xl-navbar-user-options").click(function(ev) {
        ev.stopPropagation();
    });

    $("#xl-ms-logout-menu").click(function(ev){
        ev.stopPropagation();
    });

    //Fit Sliders

    setInterval(function(){
        $(".product-details").sizeDetails();
        $(".xl-poster").sizeDetails();
        //$(".product-description").sizeCategory();
    });

    //Show Categories

    var arrow_span = $(".xl-comp-cate").find('a');

    $(arrow_span).click(function(e){
        var href = $(this).attr("href");
        if (href == "#" || href == ""){
            e.preventDefault();
        }
        $(this).siblings('span').toggleClass('rotate-span');
        $(this).siblings('ul').slideToggle();

        $(this).parent('li').siblings().find('span').removeClass('rotate-span');
        $(this).parent('li').siblings().find('ul').slideUp();
    });

    //Hover Cover

    $(".xl-modif-cover img").hover(function(){
        $(this).parent("div").addClass("xl-img-active").children("span").fadeIn();
    }, function(){
        $(this).parent("div").removeClass("xl-img-active").children("span").fadeOut();
    });

    //Hover Profil Picture

    $(".xl-profil-picture").hover(function(){
        $(this).children("div").addClass("xl-prof-up");
    }, function(){
        $(this).children("div").removeClass("xl-prof-up");
    });

    //Dotted Name Field Complete

    $("#id_name").bind('keyup, keypress, blur', function(ev){
        var comp_name = $(this).val();
            comp_name = comp_name.replace(/(^\s+|[^a-zA-Z0-9]+|\s+$)/g, "");
            comp_name = comp_name.replace(/\s+/g, "");
        $("#id_name_dotted").val(comp_name);
    });

    //Delete white space

    $("#id_user_name").bind('keyup, keypress, blur', function(ev){
        var user_name = $(this).val();
            user_name = user_name.replace(/(^\s+|[^a-zA-Z0-9]+|\s+$)/g, "");
            user_name = user_name.replace(/\s+/g, "");
        $("#id_user_name").val(user_name);
    });

    //Get Country Code

    var set_country_code = setInterval(function(){
        if($(".intl-tel-input .country-list").length > 0){
            $(".intl-tel-input .country-list li").each(function(){
                if($(this).hasClass('active')){
                    var country_code = $(this).attr("data-dial-code");
                    $("#id_phone_number").val("+"+country_code);
                }
            });
        }
    });

    setInterval(function(){
        if($("#id_phone_number").val() != ""){
            clearInterval(set_country_code);
        }else{
            setInterval(set_country_code);
        }
    });

    $(".intl-tel-input .country-list li").click(function(){
		var country_code = $(this).attr("data-dial-code");
		$("#id_phone_number").val("+" + country_code);
	});

    //Tell Input

    $("#id_phone_number").intlTelInput({
		initialCountry: "auto",
		geoIpLookup: function(callback) {
			$.get('http://ipinfo.io', function() {}, "jsonp").always(function(resp) {
				var countryCode = (resp && resp.country) ? resp.country : "";
				callback(countryCode);
			});
		},
    });

    //Edit Company Profil Img
    $("#modif_company_profil").click(function(){
        $("#id_profile_image").click();
    });

    $("#modif_user_profil").click(function(){
        $("#id_profile_image").click();
    });

    $("#id_profile_image").change(function(){
        var image = $("#profile_image");
        var button = $("#profile_edit");
        previewImage(this, image, button);
    });

    $("#profile_edit").click(function() {
        $("#update_profile_image").submit();
    });

    //Edit Company Cover Img
    $("#modif_company_cover").click(function() {
        $("#id_cover_image").click();
    });

    $("#id_cover_image").change(function(){
        var image = $("#comp_cover_image");
        var button = $("#cover_edit");
        previewCoverImage(this, image, button)
    });

    $("#cover_edit").click(function(){
        $("#update_cover_image").submit();
    })

    setInterval(function(){
        if(edit_profile == true && edit_cover == true){
            $("#profile_edit, #cover_edit").hide();
            $("#all_edit").show();
        }else{
            $("#all_edit").hide();
        }
    });

    $("#all_edit").click(function(){
        $("#update_cover_image").submit();
        $("#update_profile_image").submit();
    });

    $("#open_add_advertisment, #open_advertisment, #open_newprod_modal, #open_publish_post, #open_edit_product, #open_upload_others").magnificPopup({type:'ajax'});

    $("#close_add_product, #close_edit_product, #close_upload_others, #close_advertise-product").click(function(){
        $(".mfp-close").click();
    });

    $("#close_upload_others").click(function(){
        $(".images-upload-preview img").hide();
        $("#id_product_images_upload").val('');
    })

    $('#id_product_images_upload').on('change', function() {
        multipleImagespreview(this, 'div.images-upload-preview');
    });

    $("#add_prod_image").click(function(){
        $("#id_image").click();
    });

    //Edit Profile Modal

    $("#open_edit_profile, #open_add_address").magnificPopup({type:'ajax'});

    //Edit Post Modal

    $(window).scroll(function(){
        if($(this).scrollTop() > 320){
            $("#xl-navbar-user").addClass('xl-fix-navbar');
            $("#xl-user").css({'margin-top':'79px'});
            $(".xl-navbar-content").addClass('xl-margin-auto');
            //$("#xl-else-wrapper-else").addClass('xl-fixed-else-wrapper');
            //$("#xl-else-section-1, #xl-else-section-2").addClass('xl-else-fixed');
        }else{
            $("#xl-navbar-user").removeClass('xl-fix-navbar');
            $("#xl-user").css({'margin-top':'20px'})
            $(".xl-navbar-content").removeClass('xl-margin-auto');
            //$("#xl-else-wrapper-else").removeClass('xl-fixed-else-wrapper');
            //$("#xl-else-section-1, #xl-else-section-2").removeClass('xl-else-fixed');
        }
    });

    $("a").click(function(){
        //showLoadLinkSpinner();
    });

    $('.product-main-image').magnificPopup({
		type: 'image',
		closeOnContentClick: true,
		closeBtnInside: false,
		fixedContentPos: true,
		mainClass: 'mfp-no-margins mfp-with-zoom',
		image: {
			verticalFit: true,
            titleSrc: function(item) {
				return item.el.attr('title') + '<small>by '+item.el.attr('data-company')+'</small>';
			}
		},
		zoom: {
			enabled: true,
			duration: 300
		}
	});

    $('.other-images-popup').magnificPopup({
		delegate: 'a',
		type: 'image',
		closeOnContentClick: false,
		closeBtnInside: false,
		mainClass: 'mfp-with-zoom mfp-img-mobile',
		image: {
			verticalFit: true,
			titleSrc: function(item) {
				return item.el.attr('title') + '<small>by '+$(".other-images-popup li a").attr('data-company')+'</small>';
			}
		},
		gallery: {
			enabled: true
		},
		zoom: {
			enabled: true,
			duration: 300,
			opener: function(element) {
				return element.find('img');
			}
		}

	});

    //Load Image Main on hover

    $(".other-images-popup li a img").hover(function(){
        var image = $(this).attr("src");
        // $("#product_main_link").attr("href", image);
        // $("#product_main_image").attr("src", image);
    });

    $('#product_main_link').easyZoom();
    $(".product_else_image").easyZoom();

    //Link
    textFunctions('.post-text');
    textFunctions('.xl-product-about');

    //Follow Full

    $("#follow_company_full_now").submit(function(ev) {
        ev.preventDefault()
        $.ajax({
            type:"POST",
            url:"/company/user/follow/",
            data:{
                'company': $("input[name=company]").val(),
                'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
            },
            success:function(success){
                showSuccessMessage("company", "Company Followed !!!");
                $("#follow_success").html('<button class="follow_ok"><i class="icon ion-checkmark-round"></i> Follower</button>');
            },
            error: function(error){
                showErrorMessage("company", error);
            }
        });
    });

    $("#follow_user_full_now").submit(function(ev){
        ev.preventDefault();
        $.ajax({
            type:"POST",
            url:$(this).attr('action'),
            data:{
                'user': $("input[name=user]").val(),
                'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
            },
            success:function(success){
                showSuccessMessage("user", "User Followed !!!");
                $("#follow_success").html('<button class="follow_ok"><i class="icon ion-checkmark-round"></i> Follower</button>');
            },
            error: function(error){
                showErrorMessage("user", error);
            }
        });
    });

    //INTEREST

    $(".interess_general_product").interessProduct();

    //LIKE AND DISLIKE

    $(".general_product_like").productLike();
    $(".general_product_dislike").productDislike();

    $(".general_post_like").postLike();
    $(".general_post_dislike").postDislike();

    //Comment

    $("#comment-form").submitComment();

    //delete post

    $(".delete_single_post").deletePost();
    //slim scroll for messages

    $("#xl-messages-all").slimScroll({
        railVisible: true,
        size:'7',
        height:'calc(100vh - 227px)',
        alwaysVisible: false
    });

    //load ms product category

    $(".load_msp_category").click(function(ev){
        $("#xl-ms-product-loader").show();
        loadMSProductts($(this).attr('data-url'));
        $(this).parent('li').addClass('activated').siblings().removeClass('activated');
    });

    //Find Location

    $("#find_location").click(function(e){
		var address = $("#search_location_text").val();
		var geocoder = new google.maps.Geocoder();
		geocoder.geocode({ 'address' : address }, function (results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				var from_lat = results[0].geometry.location.lat();
				var from_long = results[0].geometry.location.lng();

                $("#latitude").val(from_lat);
				$("#longitude").val(from_long);

                var LatLng = {lat: from_lat, lng: from_long};

                map = new google.maps.Map(document.getElementById('trade_location_map'), {
				  zoom: 16,
				  center: LatLng,
                  gestureHandling: 'cooperative'
				});

				var marker = new google.maps.Marker({
				  position: LatLng,
				  map: map,
				  title: address
				});

                markers.push(marker);

                var geocoder = new google.maps.Geocoder();

                google.maps.event.addListener(map, 'click', function(event) {
                    geocoder.geocode({'latLng': event.latLng}, function(results, status) {
                        if (status == google.maps.GeocoderStatus.OK) {
                            if (results[0]) {
                                var n_address = results[0].formatted_address;
                                var n_latitude = results[0].geometry.location.lat();
                                var n_longitude = results[0].geometry.location.lng();
                                var position = {lat: n_latitude, lng: n_longitude}

                                $("#latitude").val(n_latitude);
                                $("#longitude").val(n_longitude);
                                $("#search_location_text").val(n_address);

                                clearMarkers();

                                var marker = new google.maps.Marker({
                                    position: position,
                                    map: map,
                                    title: n_address
                                });
                                markers.push(marker);
                            } else {
                                showErrorMessage("find_location", "Location Not Found");
                            }
                        } else {
                            showErrorMessage("find_location", status);
                        }
                    });
                });
			} else {
                showErrorMessage("find_location", status);
            }
		});
	});

    //Trade Status

    $("#menu-itemsstatus").activateStatus();
    $("#category_list").activateStatus();

    //slim scroll for ms list

    $(".xl-ms-scoll-pane").slimScroll({
        railVisible: true,
        size:'7',
        height:'calc(100vh - 150px)',
        alwaysVisible: false,
    });

    //search

    $(".xl-search-menu ul li a").click(function(e){
        e.preventDefault();
        $(this).parent("li").addClass("activated").siblings().removeClass("activated");
        $(".xl-search-data "+$(this).attr("data-href")).addClass("activated").siblings().removeClass("activated")
    });

    $("#xl-search-form").submit(function(e){
        e.preventDefault()
    });
    $("#xl-store-search").keyup(function(){

        var search_term = $(this).val();
        var _products = $(".xl-search-data #products").find("ul");
        var _companies = $(".xl-search-data #companies").find("ul");
        var _users = $(".xl-search-data #users").find("ul");
        $("#searh_term").text(search_term);

        if(search_term != "" && search_term != " "){
            $.ajax({
                type:'GET',
                url:'/search/?search=' + search_term,
                data:{},
                success: function(response){

                    var products = removeDuplicates(response.products);
                    var companies = removeDuplicates(response.companies);
                    var users = removeDuplicates(response.users);

                    _products.empty();
                    _companies.empty();
                    _users.empty();

                    if(products.length > 0){
                        products.forEach((product) => {
                            _products.append(`
                                <li id="search_product_${product.id}" data-tippy-interactive="true" data-tippy-placement="bottom" data-tippy-arrow="true" data-tippy-arrowtransform="scale(0.75)" data-tippy-animation="fade">
                                    <script type="text/javascript">tippy('#search_product_${product.id}', {html: document.getElementById("product_template_${product.id}")});</script>
                                    <a href="http://127.0.0.1:8000${product.url}">
                                        <div class="xl-search-main-containt">
                                            <div class="xl-search-item-img">
                                                <img src="http://127.0.0.1:8000/media/${product.image}" />
                                            </div>
                                            <div class="xl-search-item-content">
                                                <h3>${product.product_name}</h3>
                                                <p class="xl-search-comp">${product.company.name}</p>
                                                <p class="xl-search-price"><i class="icon ion-ios-pricetags"></i> ${setPriceElse(product.price)} ${product.currency}</p>
                                            </div>
                                        </div>
                                    </a>
                                    <div id="product_template_${product.id}">
                                        <div class="xl-search-hidden" style="font-size: 15px !important;" >
                                            <p style="margin-bottom: 4px; color: #eee;"><strong>Email : </strong><a style="color: #eee;" href="mailto:${product.company.email}">${product.company.email}</a></p>
                                            <p style="margin-bottom: 4px; color: #eee;">
                                                <span style="margin-right: 7px;"><i class="icon ion-ios-cart"></i> ${product.interess}</span>
                                                <span style="margin-right: 7px;"><i class="icon ion-heart"></i> ${product.likes}</span>
                                                <span><i class="icon ion-heart-broken"></i> ${product.dislikes}</span>
                                            </p>
                                            <p><strong>Distance : </strong><a style="color: #eee;" href="#">${userDistanceCompany(product.company.address)} from here</a></p>
                                        </div>
                                    </div>
                                </li>
                            `);
                        });
                    } else {
                        _products.empty().append('<p class="xl-error">NO PRODUCT FOUND</p>');
                    }

                    if(companies.length > 0){
                        companies.forEach((company) => {
                            _companies.append(`
                                <li id="search_company_${company.id}" data-tippy-interactive="true" data-tippy-placement="bottom" data-tippy-arrow="true" data-tippy-arrowtransform="scale(0.75)" data-tippy-animation="fade">
                                    <script type="text/javascript">tippy('#search_company_${company.id}', {html: document.getElementById('company_template_${company.id}')});</script>
                                    <a href="http://127.0.0.1:8000${company.url}">
                                        <div class="xl-search-main-containt">
                                            <div class="xl-search-item-img">
                                                <img src="http://127.0.0.1:8000/media/${company.profile_image}" />
                                            </div>
                                            <div class="xl-search-item-content">
                                                <h3>${company.name}</h3>
                                                <p class="xl-search-comp">@${company.name_dotted}</p>
                                                <p class="xl-search-price">${company.category}</p>
                                            </div>
                                        </div>
                                    </a>
                                    <div id="company_template_${company.id}">
                                        <div class="xl-search-hidden" style="font-size: 15px !important;" >
                                            <p style="margin-bottom: 4px; color: #eee;"><strong>Email : </strong><a style="color: #eee;" href="mailto:${company.email}">${company.email}</a></p>
                                            <p style="margin-bottom: 4px; color: #eee;">
                                                <span style="margin-right: 7px;"><i class="icon ion-ios-cart"></i> ${company.products}</span>
                                                <span style="margin-right: 7px;"><i class="icon ion-ios-compose-outline"></i> ${company.posts}</span>
                                                <span><i class="icon ion-ios-people"></i> ${company.followers}</span>
                                            </p>
                                            <p><strong>Address : </strong><a style="color: #eee;" href="#">${userDistanceCompany(company.address)} from here</a></p>
                                        </div>
                                    </div>
                                </li>
                            `)
                        });
                    } else {
                        _companies.empty().append('<p class="xl-error">NO COMPANY FOUND</p>');
                    }

                    if(users.length > 0){
                        users.forEach((user) => {
                            _users.append(`

                                <li id="search_user_${user.id}" data-tippy-interactive="true" data-tippy-placement="bottom" data-tippy-arrow="true" data-tippy-arrowtransform="scale(0.75)" data-tippy-animation="fade">
                                    <script type="text/javascript">tippy('#search_user_${user.id}', {html: document.getElementById("user_template_${user.id}")});</script>
                                    <a href="http://127.0.0.1:8000${user.url}">
                                        <div class="xl-search-main-containt">
                                            <div class="xl-search-item-img">
                                                <img src="http://127.0.0.1:8000/media/${user.profile_image}" />
                                            </div>
                                            <div class="xl-search-item-content">
                                                <h3>${user.name}</h3>
                                                <p class="xl-search-comp">@${user.username}</p>
                                                <p class="xl-search-price">${user.gender}</p>
                                            </div>
                                        </div>
                                    </a>
                                    <div id="user_template_${user.id}">
                                        <div class="xl-search-hidden" style="font-size: 15px !important;" >
                                            <p style="margin-bottom: 4px; color: #eee;"><strong>Email : </strong><a style="color: #eee;" href="mailto:${user.email}">${user.email}</a></p>
                                            <p style="margin-bottom: 4px; color: #eee;">
                                                <span style="margin-right: 7px;"><i class="icon ion-ios-cart"></i> ${user.interess}</span>
                                                <span style="margin-right: 7px;"><i class="icon ion-ios-star"></i> ${user.companies}</span>
                                                <span style="margin-right: 7px;"><i class="icon ion-ios-person"></i><i class="icon ion-ios-arrow-thin-left"></i> ${user.followers}</span>
                                                <span><i class="icon ion-ios-person"></i><i class="icon ion-ios-arrow-thin-right"></i> ${user.following}</span>
                                            </p>
                                            <p><strong>Address : </strong><a style="color: #eee;" href="#">20 km from here</a></p>
                                        </div>
                                    </div>
                                </li>
                            `)
                        });
                    } else {
                        _users.empty().append('<p class="xl-error">NO USERS FOUND</p>')
                    }
                }
            });
        } else {
            _products.empty().append('<p class="xl-error">NO PRODUCT FOUND</p>')
            _companies.empty().append('<p class="xl-error">NO COMPANY FOUND</p>')
            _users.empty().append('<p class="xl-error">NO USERS FOUND</p>')
        }
    });

    tippy('.icon');
    tippy('.picture');
    tippy('.menu-list');
    tippy('.location_tip');

    $(".xl-search-data").slimScroll({
        railVisible: true,
        size:'7',
        height:'calc(80vh - 68px)',
        alwaysVisible: false,
    });

    //Userlike category

    $(".like_category").click(function(){
        var _this = $(this);
        var category = $(this).attr("data-category");
        var url = $(this).attr("data-url");
        var user_likes = parseInt($(".sum_users").text());
        $.ajax({
            type:"POST",
            url:url,
            data:{
                "category": category,
                "csrfmiddlewaretoken":$("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(response){
                if (response == 'ok'){
                    $(".sum_users").text(user_likes + 1)
                    _this.removeClass("like_category").addClass("liked");
                    showSuccessMessage("like_category", "Category Liked !!!");
                }
            },
            error: function(error){
                showErrorMessage("like_category", error);
            }
        });
    });

    //MARKET

    $("#load_market_access").magnificPopup({type: 'ajax'});
   //  callbacks: {
   //     close: function(){
   //         alert("closed");
   //     }
   // },

    $("#access_market").click(function(e){
        e.preventDefault();
        var company = $(this).attr("data-company");
        var url = $(this).attr("data-href");
        var user = $(this).attr("data-user");
        var check_url = $(this).attr("data-check-url");
        var market_url = $(this).attr("data-market-products");
        var error_access = $(this).attr("data-error-access");

        $.ajax({
            type: "POST",
            url: url,
            data: {"company": company, "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()},
            success: function(response){
                if(response == "ok"){
                    $("#load_market_access").click();
                    $.get(check_url, function(data){
                        var jdata = JSON.parse(data);
                        if (jdata.status == "vip"){
                            load_market_product(market_url + "?key="+jdata.key);
                        } else if (jdata.status == "blocked"){
                            load_market_product(error_access + "?key="+jdata.key);
                        } else {
                            socket.emit("askAccess", jdata)
                        }
                    });
                }else{
                    $.alert({theme:'material',title:'Error',icon:'icon ion-close-circled',content:response,type: 'red'});
                }
            },
            error: function(error){
                showErrorMessage("access_market", error);
            }
        });
    });
});

jQuery.fn.interessProduct = function(){
    $(this).click(function(ev){
        var product = $(this).attr('data-product');
        $.ajax({
            type:'POST',
            url: $(this).attr('data-url'),
            data:{
                'product':product,
                'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
            },
            success:function(success){
                showSuccessMessage("product_interess", "Product Interested !!!");
                $('#after_interess'+product).html("<i class='icon ion-ios-cart interessed'></i>");
                $('#interess_after_else'+product).html("<button style='background:lightgreen;' type='button'><i class='icon ion-checkmark-round'></i> Interested</button>");
                $(".product-menu-items"+product).fadeOut();
                $(".after_interess"+product).html('<span class="interessed"><i class="icon ion-ios-cart"></i></span>');
                $(".interess_general_product_else"+product).parent('li').hide();
                $(".interess_after_else"+product).html('<button style="background:lightgreen;" type="button"><i class="icon ion-checkmark-round"></i> Interest</button>');
                $(".general_sum_interess"+product).text(parseInt($(".general_sum_interess"+product).text()) + 1);
            },
            error: function(error){
                showErrorMessage("product_interess", error);
            }
        });
    });
}

jQuery.fn.productLike = function (){
    $(this).click(function(){
        var product = $(this).attr('data-product')
        var mention = "like";
        if($(this).hasClass('liked')){}
        else{
            $.ajax({
                type:'POST',
                url:$(this).attr('data-href'),
                data:{
                    'product':product,
                    'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val(),
                    'mention':mention
                },
                success:function(success){
                    $(".general_product_like"+product).addClass('liked');
                    $(".product_sum_like"+product).text(parseInt($(".product_sum_like"+product).text()) + 1);
                    if($(".general_product_dislike"+product).hasClass('disliked')){
                        $(".general_product_dislike"+product).removeClass('disliked');
                        $(".product_sum_dislike"+product).text(parseInt($(".product_sum_dislike"+product).text()) - 1);
                    }
                    showSuccessMessage("product_like", "Product Liked !!!");
                },
                error: function(error){
                    showErrorMessage("product_like", error);
                }
            });
        }
    });
}

jQuery.fn.productDislike = function(){
    $(this).click(function(){
        var product = $(this).attr('data-product')
        var mention = "dislike";
        if($(this).hasClass('disliked')){}
        else{
            $.ajax({
                type:'POST',
                url:$(this).attr('data-href'),
                data:{
                    'product':product,
                    'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val(),
                    'mention':mention
                },
                success:function(){
                    $(".general_product_dislike"+product).addClass('disliked');
                    $(".product_sum_dislike"+product).text(parseInt($(".product_sum_dislike"+product).text()) + 1);
                    if($(".general_product_like"+product).hasClass('liked')){
                        $(".general_product_like"+product).removeClass('liked');
                        $(".product_sum_like"+product).text(parseInt($(".product_sum_like"+product).text()) - 1);
                    }
                    showSuccessMessage("product_dislike", "Product Disliked !!!");
                },
                error: function(error){
                    showErrorMessage("product_dislike", error);
                }
            });
        }
    });
}

jQuery.fn.postLike = function(){
    $(this).click(function(){
        var post = $(this).attr('data-post')
        var mention = "like";
        if($(this).hasClass('liked')){}
        else{
            $.ajax({
                type:'POST',
                url:$(this).attr('data-href'),
                data:{
                    'post':post,
                    'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val(),
                    'mention':mention
                },
                success:function(success){
                    $(".general_post_like"+post).addClass('liked');
                    $(".post_sum_like"+post).text(parseInt($(".post_sum_like"+post).text()) + 1);
                    if($(".general_post_dislike"+post).hasClass('disliked')){
                        $(".general_post_dislike"+post).removeClass('disliked');
                        $(".post_sum_dislike"+post).text(parseInt($(".post_sum_dislike"+post).text()) - 1);
                    }
                    showSuccessMessage("post_like", "Post Liked !!!");
                },
                error: function(error){
                    showErrorMessage("post_like", error);
                }
            });
        }
    });
}

jQuery.fn.postDislike = function(){
    $(this).click(function(){
        var post = $(this).attr('data-post')
        var mention = "dislike";
        if($(this).hasClass('disliked')){}
        else{
            $.ajax({
                type:'POST',
                url:$(this).attr('data-href'),
                data:{
                    'post':post,
                    'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val(),
                    'mention':mention
                },
                success:function(success){
                    $(".general_post_dislike"+post).addClass('disliked');
                    $(".post_sum_dislike"+post).text(parseInt($(".post_sum_dislike"+post).text()) + 1);
                    if($(".general_post_like"+post).hasClass('liked')){
                        $(".general_post_like"+post).removeClass('liked');
                        $(".post_sum_like"+post).text(parseInt($(".post_sum_like"+post).text()) - 1);
                    }
                    showSuccessMessage("post_dislike", "Post Liked !!!")
                },
                error: function(error){
                    showErrorMessage("post_dislike", error);
                }
            });
        }
    });
}

jQuery.fn.deletePost = function(){
    $(this).click(function(){
        var url = $(this).attr('data-href');
        var post = $(this).attr('data-post');
        $.confirm({
            title: 'Delete Post',
            content: 'Do you really want to delete this post ???',
            icon: 'icon ion-help-circled',
            animation: 'scale',
            theme:'material',
            type:'blue',
            closeAnimation: 'scale',
            opacity: 0.5,
            buttons:{
                'confirm':{
                    text: 'Yes',
                    btnClass: 'btn-green',
                    action: function(){
                        $.ajax({
                            type:'POST',
                            url:url,
                            data:{
                                'post': post,
                                'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
                            },
                            success:function(success){
                                $("#xl-main-post"+post).fadeOut();
                                $.alert({theme:'material',title:'Success',icon:'icon ion-checkmark-circled',content:'Post Deteled Successfully !!!',type: 'green'});
                                showSuccessMessage("delete_post", "Post Deleted !!!");
                            },
                            error: function(error){
                                showErrorMessage("delete_post", error);
                            }
                        });
                    }
                },
                cancel:function(){
                },
            }
        });
    });
}

jQuery.fn.submitComment = function(){
    autosize($(this).children("textarea"));
    $(this).submit(function(ev){
        ev.preventDefault();
        var url = $(this).attr('action');
        var product = $(this).attr('data-product');
        var comment_text = $("textarea[name=comment_text]").val();
        var comment_url = $(this).attr('comments-loader-url');
        if(comment_text != ''){
            $.ajax({
                type:'POST',
                url:url,
                data:{
                    'product':product,
                    'text':comment_text,
                    'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
                },
                success:function(success){
                    $("textarea[name=comment_text]").val('');
                    loadProductComments(comment_url);
                    setTimeout(function(){
                        $('.comments_list' + product).load(comment_url, function(error){showErrorMessage('load_replies', error);});
                    }, 100);
                    showSuccessMessage("comment_product", "Comment Added !!!");
                },
                error: function(error){
                    showErrorMessage("comment_product", error);
                }
            });
        }else{
            $.alert({theme:'material',title:'Error',icon:'icon ion-close-circled',content:'Comment Text is Empty !!!',type: 'red'});
        }
    });
}

jQuery.fn.followCompany = function(){
    $(this).submit(function(ev){
        ev.preventDefault();
        var company = $(this).attr("data-company");
        var url = $(this).attr("action");
        $.ajax({
            type:"POST",
            url:url,
            data:{
                'company': $("#company" + company).val(),
                'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
            },
            success:function(success){
                showSuccessMessage("success", "Company Followed !!!");
                $("#follow_success" + company).html('<button class="follow_ok"><i class="icon ion-checkmark-round"></i></button>');
            },
            error: function(error){
                showErrorMessage("error", error);
            }
        });
    });
}

//load comments

function loadProductComments(url){
    if(url != "" && url != "#"){
        setTimeout("$('#comments-list').load('" + url + "', function(){$('#comment_loader').hide();}, function(error){showErrorMessage('load_error', error);})");
    }
}

function loadEditReply(url){
    if(url != "" && url != "#"){
        setTimeout("$('#edit_reply_cont').load('" + url + "', function(){$('#edit_reply_loader').hide();}, function(error){showErrorMessage('load_error', error);})");
    }
}

//load trade messages

function loadTradeMessages(url){
    if(url != "" && url != "#"){
        setTimeout("$('#xl-messages-all').load('" + url + "', function(){$('#messages_loader').hide();}, function(error){showErrorMessage('load_error', error);})");
        updateMessageScroll();
    }
}

function updateMessageScroll(){
    var message_list = $("#xl-messages-all");
    message_list.scrollTop = message_list.scrollHeight;
    $("#xl-messages-all").animate({ scrollTop: 100000000}, 1000);
}

//load product ms

function loadMSProductts(url){
    if(url != "" && url != "#"){
        setTimeout("$('#xl-ms-product-wrapper').load('" + url + "', function(){$('#xl-ms-product-loader').hide();}, function(error){showErrorMessage('load_error', error);})");
    }
}

function loadMSCurrentBill(url){
    if(url != "" && url != "#"){
        setTimeout("$('#xl-ms-bill-wrapper').load('" + url + "', function(){$('#xl-ms-bill-loader').hide();}, function(error){showErrorMessage('load_error', error);})");
    }
}

function load_msp_products(url){
    if(url != "" && url != "#"){
        setTimeout("$('#msp_product_wrapper').load('" + url + "', function(){$('#msp_products_loader').hide();}, function(error){showErrorMessage('load_error', error);})");
    }
}

function load_trades_lists(url){
    if(url != "" && url != "#"){
        setTimeout("$('#trade_list_wrapper').load('" + url + "', function(){$('#trade_list_loader').hide();}, function(error){showErrorMessage('load_error', error);})");
    }
}

function load_market_product(url){
    if(url != "" && url != "#"){
        setTimeout("$('#xl_market_products').load('" + url + "', function(){$('#loading_await_market').hide();}, function(error){showErrorMessage('load_error', error);})");
    }
}

function load_shopping_cart(url){
    if(url != "" && url != "#"){
        setTimeout("$('#xl_shopping_cart').load('" + url + "', function(){$('#loading_await_market').hide();}, function(error){showErrorMessage('load_error', error);})");
    }
}

function showWaitMessage(){
    $.dialog({
        title: '',
        lazyOpen: true,
        content: '<div style="text-align: center;">'+
                '<img src="http://127.0.0.1:8000/static/images/loading.gif" style="width:30px; height: 30px;"/>'+
                '<br/><h2>PLEASE WAIT...</h2></div>'
    });
}

jQuery.fn.finishShoppingCart = function(){

    $(this).click(function(){

        var finish_url = $(this).attr("data-finish-url");
        var pay_url = $(this).attr("data-pay-url");
        var data_href = $(this).attr("data-href");
        var cart_url = $(this).attr("data-cart-url");
        var market_status = $(this).attr("data-market-status");
        var user = $(this).attr("data-user");

        $.confirm({
            title: 'Finish Shopping Cart',
            content: 'Do you really want to ' + $(this).text() + ' ???',
            icon: 'icon ion-help-circled',
            animation: 'scale',
            theme:'material',
            type:'blue',
            closeAnimation: 'scale',
            opacity: 0.5,
            buttons:{
                'confirm':{
                    text: 'Yes',
                    btnClass: 'btn-green',
                    action: function(){
                        $.ajax({
                            type:'GET',
                            url: cart_url,
                            data: {},
                            success: function(response){
                                var data = JSON.parse(response);

                                if(data.status == "finished"){
                                    socket.emit("finishCart", data);
                                    showWaitMessage();
                                } else if (data.status == "accepted"){
                                    $("#finish_pay_cart_bill").fadeIn();
                                } else {
                                    showWaitMessage();
                                    $.ajax({
                                        type: 'GET',
                                        url: finish_url,
                                        data: {},
                                        success: function(response){
                                            if (response == "ok"){
                                                socket.emit("finishCart", data);
                                            } else {
                                                $("body").find(".jconfirm-closeIcon").click();
                                                $.alert({theme:'material',title:'Error',icon:'icon ion-close-circled',content:response,type: 'red'});
                                            }
                                        },
                                        error: function(error){
                                            showErrorMessage("error", error);
                                        }
                                    });
                                }
                            },
                            error: function(error){

                            }
                        });
                    }
                },
                cancel:function(){},
            }
        });
    });
}

//Capitalize

 function capitalize(text){
    var text = text.toString();
    return text.replace(text.charAt(0), text.charAt(0).toUpperCase())
}

//Fit Slidders

jQuery.fn.sizeDetails = function(){
    var width = $(this).parent().width();
    $(this).css({
        'width': width - 14
    });
}

jQuery.fn.activateStatus = function(){
    var status = $(this).attr("data-status");
    var status_link = $(this).find("li").children("a");
    for(var i = 0; i <= status_link.length; i++){
        if($(status_link[i]).attr("data-status") == status){
            $(status_link[i]).parent("li").addClass("li_acivated").siblings().removeClass("li_acivated");
        }
    }
}

jQuery.fn.showMenu = function (){
    var id = $(this).attr("data-id");
    $(window).click(function(e){
        $("#menu-items" + id).fadeOut();
    });
    $("#menu-items" + id).click(function (ev) {
        ev.stopPropagation();
    });
    $(this).click(function(ev){
        ev.stopPropagation();
        $("#menu-items" + id).fadeIn();
    });
}


function sizeCategory(container){
    var height = $(container).height();
    $(container + " .product-description").css({
        'height': height
    });
}

function showErrorMessage(id, message){
    iziToast.error({
        id: id,
        title: 'Error',
        message: message,
        position: 'bottomLeft',
        transitionIn: 'bounceInLeft',
        close: false,
    });
}

function showSuccessMessage(id, message){
    iziToast.success({
        id: id,
        timeout: 3000,
        title: 'Success',
        message: message,
        position: 'bottomLeft',
        transitionIn: 'bounceInLeft',
        close: false,
    });
}

//Preview Image

function previewImage(input, img, button) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var ext = $(input).val().split('.').pop().toLowerCase();
            var extVid = $(input).val().split('.').pop();
            if($.inArray(ext, ['gif','png','jpg','jpeg']) > 0) {
                $(img).attr('src', e.target.result);
                $(button).show();
                edit_profile = true;
            }else{
                $.alert({theme:'material',title:'Error',icon:'icon ion-close-circled',content:'Please, Insert Only Image',type: 'red'});
                $(button).hide();
                edit_profile = false;
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function previewCoverImage(input, img, button) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var ext = $(input).val().split('.').pop().toLowerCase();
            var extVid = $(input).val().split('.').pop();
            if($.inArray(ext, ['gif','png','jpg','jpeg']) > 0) {
                $(img).css({
                    "background": "url('" + e.target.result + "')",
                    "background-size":"cover",
                    "background-repeat":"no-repeat",
                    "background-position":"center"
                });
                $(button).show();
                edit_cover = true;
            }else{
                $.alert({theme:'material',title:'Error',icon:'icon ion-close-circled',content:'Please, Insert Only Image',type: 'red'});
                $(button).hide();
                edit_cover = false;
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function multipleImagespreview(input, placeToInsertImagePreview) {
    if (input.files) {
        var filesAmount = input.files.length;
        if (filesAmount <= 5){
            for (i = 0; i < filesAmount; i++) {
                var reader = new FileReader();
                reader.onload = function(event) {
                    $($.parseHTML('<img>')).attr('src', event.target.result).appendTo(placeToInsertImagePreview).css({'width':'calc((100% - '+ 7 * (filesAmount - 1) +'px) / '+ filesAmount +')'});
                }
                reader.readAsDataURL(input.files[i]);
            }
        }else{
            $("#id_product_images_upload").val('');
            $.alert({theme:'material',title:'Error',icon:'icon ion-close-circled',content:'Upload Maximum 5 images only',type: 'red'});
        }
    }
}

function previewPostImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var ext = $(input).val().split('.').pop().toLowerCase();
            if($.inArray(ext, ['img','gif','png','jpg','jpeg','svg']) > 0) {
                $("#id_file_type").val('picture')
                $("#preview_post_image").attr('src', e.target.result).show();
                $("#preview_post_video").hide()
            }else if($.inArray(ext, ['fvl','mp4','webm','m4v','mpeg', 'mkv', 'mov']) > 0){
                $("#id_file_type").val('video')
                $("#preview_post_video").attr('src', e.target.result).show();
                $("#preview_post_image").hide();
            }else{
                $.alert({theme:'material',title:'Error',icon:'icon ion-close-circled',content:'Please, Insert Only Image',type: 'red'});
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function previewReplyImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var ext = $(input).val().split('.').pop().toLowerCase();
            if($.inArray(ext, ['img','gif','png','jpg','jpeg','svg']) > 0) {
                $("#preview_reply_image").attr('src', e.target.result).show();
            }else{
                $.alert({theme:'material',title:'Error',icon:'icon ion-close-circled',content:'Please, Insert Only Image',type: 'red'});
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

//Time

jQuery.fn.setTime = function(){
    setInterval(() => {
        var time = $(this).attr("data-time");
        var utc_timestamp = (Date.parse(time)) - (new Date().getTimezoneOffset() * 60 * 1000);
        var hours_check = new Date(utc_timestamp).getHours();

        var post_time = utc_timestamp / 1000;
    	var timee =  utc_timestamp;
        var current_time = Math.floor(jQuery.now() / 1000);

        real_time = (current_time - post_time);
        if (real_time < 60) {
            $(this).text('Just Now');
        }else if (real_time >= 60 && real_time < 3600) {
            time_be = moment(timee).fromNow();
            $(this).text(time_be);
        }else if (real_time >= 3600 && real_time < 86400) {
            time_be = moment(timee).fromNow();
            $(this).text(time_be);
        }else if (real_time >= 86400 && real_time < 604800) {
            time_b = Math.floor(real_time / (60 * 60 * 24));
            time_be = moment(timee).calendar();
            $(this).text(time_be);
        }else if (real_time >= 604800 && real_time < 31104000 ) {
            time_be = moment(timee).format('MMMM Do [at] h:mm a');
            $(this).text(time_be);
        }else{
            time_be = moment(timee).format('DD MMM YYYY [at] h:mm a');
            $(this).text(time_be);
        }
        return false;
    }, 100);
}

//Numbers

function setNumbers(container, price){
    var number = parseInt(price);
    var number_set = numeral(number).format('0.0a');
    $(container).text(number_set);
}

function setPrice(container, price){
    var number = parseInt(price);
    var number_set = numeral(number).format('0.0a');
    $(container).text(number_set);
}

function setPriceElse(price){
    var number = parseInt(price);
    var number_set = numeral(number).format('0.0a');
    return number_set
}

//category slide

function slideCategory (container){

    var left_button = $(container).children('.xl-left-items');
    var right_button = $(container).children('.xl-right-items');
    var ul_width = 0;
    var container_width = $(container).width();
    var list_length = $(container + " ul li").length;
    var slide_time = 500;
    var slide_count = 0;

    $(container + " ul li").each(function(){
        ul_width += $(this).width();
    });

    var slide_width = ul_width - container_width;

    $(container).hover(function(){
        $(container).children('button').fadeIn();
    }, function(){
        $(container).children('button').fadeOut();
    });

    var mesure = slide_width / (list_length - 1);

    right_button.click(function(){
        if(slide_width > 0){
            $(container + " ul").animate({
                marginLeft: '-='+mesure+'px'
            }, slide_time);
            slide_count++;
            slide_width = slide_width - mesure;
        }
    });

    left_button.click(function(){
        if(slide_count > 0){
            $(container + " ul").animate({
                marginLeft: '+='+mesure+'px'
            }, slide_time);
            slide_count--;
            slide_width = slide_width + mesure;
        }
    });
}

//Linkify

linkify_hashtag=function(t){
	t = t.replace(/(^|)#(\w+)/gi,function (s){
		return '<b><a rel="load_page" href="/search/?key='+s.replace(/#/,'') +'">'+s+'</a></b>';
	});
	return t.replace(/\/@/gi,"/" );
}

linkify_username=function(t){
	t = t.replace(/(^|)@(\w+)/gi,function (s){
		return '<b><a href="/user/'+s.replace(/@/,'') +'/">'+s+'</a></b>';
	});
	return t.replace(/\/@/gi,"/" );
}

function textFunctions(cont){
	var txt = $(cont).text();
	$(cont).each(function(){$(this).html(linkify_hashtag($(this).html()));});
	$(cont).linkify({target: "_blank"});
	//$(cont).each(function(){$(this).html(linkify_username($(this).html()));});
}

//Get cookie

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function printBill() {
    var bill = document.getElementById("bill_or_receipt");
    var bill_content = window.open('', '', 'height=500', 'width=1200');
    bill_content.document.write('<html><head><title>Receipt &amp; Bill</title><body>');
    bill_content.document.write(bill.innerHTML);
    bill_content.document.write('</body></html>');
    bill_content.document.close();
    setTimeout(function () {
        bill_content.print();
    });
    return false;
}

function hoverImage(a,b){
    $(a).hover(function(){
        $(this).find(b).css({"opacity":0.9,"-webkit-transform":"scale(1,1)","-ms-transform":"scale(1,1)","-moz-transform":"scale(1,1)","transform":"scale(1,1)"});
    },function(){
        $(this).find(b).css({"opacity":0,"-webkit-transform":"scale(0,0)","-ms-transform":"scale(0,0)","-moz-transform":"scale(0,0)","transform":"scale(0,0)"});
    });
}

function removeDuplicates(array){
    let unique_array = array.filter(function(elem, index, self) {
        return index == self.indexOf(elem);
    });
    return unique_array
}

function showLoadLinkSpinner(){
    $("#header_image").attr("src", "http://127.0.0.1:8000/static/images/loading.gif");
}

function hideLoadLinkSpinner(){
    $("#header_image").attr("src", "http://127.0.0.1:8000/static/images/store.png");
}

//Send Location Functions

function InitializePlaces(input){
    var autocomplete = new google.maps.places.Autocomplete(document.getElementById(input));
    google.maps.event.addListener(autocomplete, 'place_changed', function(){
        autocomplete.getPlace();
    });
}

function getUserCurrentLocation(lat, long, addr){
    if(!navigator.geolocation){
        return alert('Geolocation not supported by your browser');
    }
    navigator.geolocation.getCurrentPosition(function(position){

        var geocoder = new google.maps.Geocoder();
        var location = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

        geocoder.geocode({'latLng': location}, function(results, status){
            if (status == google.maps.GeocoderStatus.OK) {
                var latitude =  position.coords.latitude;
                var longitude = position.coords.longitude;
                var address = results[0].formatted_address;

                document.getElementById(lat).value = latitude;
                document.getElementById(long).value = longitude;
                document.getElementById(addr).value = address;

            } else {
                showErrorMessage("locate_user", status);
            }
        });
    }, function(){
        showErrorMessage("locate_user", 'Unable to fetch location');
    });
}

function initMapUser() {
    
	var latitude = parseFloat($("#latitude").val());
	var longitude = parseFloat($("#longitude").val());
	var address = $("#search_location_text").val();
    var myLatLng = {lat: latitude, lng: longitude};

    map = new google.maps.Map(document.getElementById('trade_location_map'), {
        zoom: 16,
        center: myLatLng,
        gestureHandling: 'cooperative'
    });

    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: address
    });

    markers.push(marker);

    var geocoder = new google.maps.Geocoder();

    google.maps.event.addListener(map, 'click', function(event) {
        geocoder.geocode({'latLng': event.latLng}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[0]) {
                    var n_address = results[0].formatted_address;
                    var n_latitude = results[0].geometry.location.lat();
                    var n_longitude = results[0].geometry.location.lng();
                    var position = {lat: n_latitude, lng: n_longitude}

                    $("#latitude_else").val(n_latitude);
                    $("#longitude_else").val(n_longitude);
                    $("#search_else").val(n_address);

                    clearMarkers();

                    var marker = new google.maps.Marker({
                        position: position,
                        map: map,
                        title: n_address
                    });
                    markers.push(marker);
                }
            } else {
                showErrorMessage("init_map", status);
            }
        });
    });
}

function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

function clearMarkers() {
    setMapOnAll(null);
}

function deleteMarkers() {
    clearMarkers();
    markers = [];
}

function loadMapMessage(container, address, longitude, latitude){
    var myLatLng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
    var map = new google.maps.Map(document.getElementById(container), {
        zoom: 16,
        center: myLatLng,
        gestureHandling: 'cooperative'
    });
    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: address
    });
}

function calculateDistance(end, start){
    return (google.maps.geometry.spherical.computeDistanceBetween(end, start) / 1000).toFixed(2);
}

function userDistanceCompany(address) {
    if (address.length > 0){
        var latitude = address[0].latitude;
        var longitude = address[0].longitude
        var start = new google.maps.LatLng(parseFloat($("#gen_lat").val()), parseFloat($("#gen_lon").val()));
        var end = new google.maps.LatLng(latitude, longitude);

        return latitude && longitude ? calculateDistance(end, start) + " km" : null
    } else {
        return "undefined"
    }

}

function drawRouteMap(latitude, longitude, address, container, id, mode){
    var directionsDisplay;
    var directionsService = new google.maps.DirectionsService();
    var map;

    directionsDisplay = new google.maps.DirectionsRenderer();
    var myLatLng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
    map = new google.maps.Map(document.getElementById(container), {
        zoom: 17,
        center: myLatLng,
        gestureHandling: 'cooperative'
    });

    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: address
    });

    var from_lat = parseFloat($("#latitude_else").val());
    var from_long = parseFloat($("#longitude_else").val());
    var from_address = $("#search_else").val();

    var end = new google.maps.LatLng(parseFloat(latitude), parseFloat(longitude));
    var start = new google.maps.LatLng(from_lat, from_long);

    $("#distance_"+id).text(calculateDistance(end, start) + " km");

    var service = new google.maps.DistanceMatrixService();
    var bounds = new google.maps.LatLngBounds();

    bounds.extend(start);
    bounds.extend(end);
    map.fitBounds(bounds);

    if (mode == "d"){
        service.getDistanceMatrix({
            origins: [from_address],
            destinations: [address],
            travelMode: 'DRIVING',
            drivingOptions: {
                departureTime: new Date(Date.now()),
                trafficModel: 'optimistic'
            },
            unitSystem: google.maps.UnitSystem.METRIC,
            avoidHighways: true,
            avoidTolls: true,

        }, function(response){
            var time_drive = response.rows[0].elements[0].duration.text;
            var time_with_traffic = response.rows[0].elements[0].duration_in_traffic.text;
            var distance = response.rows[0].elements[0].distance.text;
            $("#time").text(time_drive);
            $("#with_traffic").show();
            $("#time_drive_traffic").text(time_with_traffic + " (with traffic)");
            $("#distance_"+id).text(distance);
        });

        var request = {
            origin: start,
            destination: end,
            travelMode: google.maps.TravelMode.DRIVING
        };

        directionsService.route(request, function (response, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                directionsDisplay.setDirections(response);
                directionsDisplay.setMap(map);
            } else {
                 showErrorMessage("draw_routes", status);
            }
        });

    } else if (mode == "w"){
        service.getDistanceMatrix({
            origins: [from_address],
            destinations: [address],
            travelMode: 'WALKING',
            drivingOptions: {
                departureTime: new Date(Date.now()),
                trafficModel: 'optimistic'
            },
            unitSystem: google.maps.UnitSystem.METRIC,
            avoidHighways: true,
            avoidTolls: true,

        }, function(response){
            var time_walk = response.rows[0].elements[0].duration.text;
            var distance = response.rows[0].elements[0].distance.text;
            $("#time").text(time_walk);
            $("#distance_"+id).text(distance);
            $("#with_traffic").hide();
        });

        var request = {
            origin: start,
            destination: end,
            travelMode: google.maps.TravelMode.WALKING
        };

        directionsService.route(request, function (response, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                directionsDisplay.setDirections(response);
                directionsDisplay.setMap(map);
            } else {
                showErrorMessage("draw_routes", status);
            }
        });

    } else {
        showErrorMessage("draw_routes", `Unknown Mode ${mode}`);
    }
}
