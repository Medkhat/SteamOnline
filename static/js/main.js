  $(document).ready(function () {
    $("#lbtn").click(function () {
      $(".lang_dd_links").toggleClass('fd_block');

      if ($(".dd_links").hasClass("d_block")) {
        $(".dd_links").removeClass("d_block");
      }
    });

    $("#user_img").click(function () {
      $(".dd_links").toggleClass("d_block");

      if ($(".lang_dd_links").hasClass("fd_block")) {
        $(".lang_dd_links").removeClass("fd_block");
      }
    });

    $("#resPassBtn").click(function () {
      var rpi_value1 = $("#resPass1").val();
      var rpi_value2 = $("#resPass2").val();

      if (rpi_value1 != rpi_value2) {
        $(".check_text").text("Пароли не совпадают!");
        $("#resPass1").val("");
        $("#resPass2").val("");
      }
    });

    $("#add_stud_btn").click(function () {
      var spi_value1 = $("#stud_pass_1").val();
      var spi_value2 = $("#stud_pass_2").val();

      if (spi_value1 != spi_value2) {
        $(".add_check_text").text("Пароли не совпадают!");
        $("#resPass1").val("");
        $("#resPass2").val("");
      }
    });

    $(".reset_pas_link").click(function () {
      $("#resPassTitle").text("Сброс пароля - " + $(this).data('name'));
    });

    $("#img_upload").on("change", function (e) {
      var fname = e.target.files[0].name;
      $("#img_up").modal('show');
      $(".img_f_name").text(fname);
    });

    $("#uploadVideo").on("change", function(e){
      var vname = e.target.files[0].name;
      $("#vidUp").modal('show');
      $("#vname").text(vname);
    });

    $("#add_header_video").click(function(){
      $(".ac_video_block").css({'display':'block'});
      $(".label_input").css({'display':'none'});
      $("#vidUp").modal('hide');
    });

    var radioName;

    $("#data_3 input").on("change", function() {
      radioName = $('input[name=sert]:checked', '#data_3').val();
    });

    $("#editCourseBtn").click(function(){
      $("#data1").text($("#data_1").val());
      $("#data2").text($("#data_2").val());
      $("#data4").text($("#data_4").val());
      $("#data3").text(radioName);
      $("#editCourseData").modal("hide");
    });

    $(window).resize(function () {
      
      var width = $(window).width();

      if (width < 417) {

        $("#lbtn").text("kz");
        $("#kz").text("kz");
        $("#ru").text("ru");

        $("#modallg, #modallg2").removeClass("modal-lg");

      } else {

        $("#lbtn").text("Қазақша");
        $("#kz").text("Қазақша");
        $("#ru").text("Орысша");

        $("#modallg, #modallg2").addClass("modal-lg");

      }

      

    });

    var fixed_block = $(".cd_left_block").offset().top;
    // var fb_width = $(".cd_left_block").outerWidth();
    // var fb2_width = $(".help_block").outerWidth();

    $(window).scroll(function () {
      $(".fixed_block").css(
        {
          'position': 'sticky',
          'position': '-webkit-sticky',
          'top': '90px',
        }
      );
      $(".fixed_block_2").css(
        {
          'position': 'sticky',
          'position': '-webkit-sticky',
          'top': '100px',
        }
      );

      if ($(window).width() > 991) {
        if ($(window).scrollTop() > fixed_block) {
          $(".cd_left_block").addClass("fixed_block");
          $(".help_block").addClass("fixed_block_2");

        } else {
          $(".cd_left_block").removeClass("fixed_block");
          $(".help_block").removeClass("fixed_block_2");
        }
      }
    });

  });

  $("button#courseTitleBtn").click(function(){
    var courseTitle = $("input#courseTitleInput").val();
    $("h4#courseTitleLocation").text(courseTitle).css({'color':'#000000'});
    $("#courseTitle").modal('hide');
  });

  $("#uplVideoForLess").on("change", function (e) {
    var uvname = e.target.files[0].name;
    $(".uvn span").text(uvname);
    $("#uvlabel").css({'display':'none'});
    $(".uvn").css(
      {
        'display':'flex',
        'justify-content':'space-between',
        'align-items':'center'
      }
    );
    $("#saveuv, #uploadedVideoPlayer, #videoTitleInput, #addPosterForLessVideoDiv").css({'display':'block'});
  });

  window.reset = function(e) {
    e.wrap('<form>').closest('form').get(0).reset();
    e.unwrap();
    $(".uvn, #saveuv, #uploadedVideoPlayer, #videoTitleInput, #addPosterForLessVideoDiv").css({'display':'none'});
    $("#uvlabel").css({'display':'inline'});
  }

  $(document).ready(function(){
    $(".delete_teachers, .deleteLessBtn, .delete_table_teachers").click(function(){
      $(".delete_teacher_btn").attr('href', $(this).data('url'));
    });

    $("#uploadPoster").on("change", function(e){
      var posterName = e.target.files[0].name;
      $("#posterUpload").modal('show');
      $("#posterName").text(posterName);
    });

    $("#sertificate").on("change", function(e){
      var sert_name = e.target.files[0].name;
      $(".sertif_name").css({'display':'block'}).text(sert_name);
    });
        
  });

