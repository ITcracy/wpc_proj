$(document).ready(function() {
function twitter_widget(){
user_name = $("#twitter_username").val()
tweet_limit = $("#tweet_limit").val()
console.log("username: ",user_name);
console.log("limit: ", tweet_limit);
if(user_name && tweet_limit)
{
$("#twitter_block").html('<a class="twitter-timeline" href="https://twitter.com/'+user_name+'" data-theme="dark" data-height="15" data-width="300"  data-chrome="" data-tweet-limit="'+tweet_limit+'">Tweets by '+user_name+'</a>');
}
}

$(window).bind("load",twitter_widget() );

}
)