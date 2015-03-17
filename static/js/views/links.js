var app = angular.module('LinksList', ['infinite-scroll', 'ngTagsInput'])

app.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller("LinksListController", ['$scope', '$http',
    function ($scope, $http) {
        $scope.links = [];
        $scope.nextPage = "";
        $scope.busy = false;
        $scope.searchOption = "Search Tags";
        $scope.searchMode = false;
        $scope.orderOptions = [
            {name: "Latest", query: "latest"},
            {name: "Most Liked", query: "likes"}
        ];
        $scope.orderOption = $scope.orderOptions[0];
        $scope.tags = [];
        $scope.searchQuery = {q: ""};
        $scope.pollAllLinks = function () {
            $scope.busy = true;
            var queryUrl = "api/allbookmarks/?format=json&order=" + $scope.orderOption.query;
            if ($scope.searchMode) {
                if ($scope.tags.length > 0 && $scope.searchOption === "Search Tags") {
                    tagNames = jQuery.map($scope.tags, function (t, i) {
                        return ( t.name );
                    });
                    queryUrl = queryUrl + "&tags=" + tagNames.toString();
                }
                else if ($scope.searchQuery.q && $scope.searchOption === "Search Text") {
                    queryUrl = queryUrl + "&q=" + $scope.searchQuery.q;
                }
            }


            var requestUrl = $scope.nextPage == "" ? baseUrl + queryUrl : $scope.nextPage;

            if ($scope.nextPage != null) {
                $http
                    .get(requestUrl)
                    .success(function (data, status) {
                        $scope.nextPage = data.next;
                        var items = data.results;
                        for (var i = 0; i < items.length; i++) {
                            $scope.links.push(items[i]);
                        }

                        $scope.busy = false;
                    });
            }
            else {
                $scope.busy = false;
            }

        };

        $scope.addTag = function (tag) {
            $scope.push(tag);
        };

        $scope.changeSearchOption = function (option) {
            $scope.searchOption = option;
        };

        $scope.search = function () {
            $scope.nextPage = "";
            $scope.links = [];
            if ($scope.tags.length > 0 && $scope.searchOption === "Search Tags") {
                $scope.links = [];
                $scope.searchMode = true;
                $scope.pollAllLinks();
            }
            else if ($scope.searchQuery.q && $scope.searchOption === "Search Text") {
                $scope.links = [];
                $scope.searchMode = true;
                $scope.pollAllLinks();
            }
            else {
                $scope.searchMode = false;
                $scope.pollAllLinks();
            }

        };

        $scope.filterByTag = function (item) {
            $scope.searchOption = "Search Tags";
            $scope.tags = [item];
            $scope.search();
        };

        $scope.loadTags = function (query) {
            return $http.get(baseUrl + "api/alltags/?format=json&q=" + query);
        };

        $scope.likeClick = function (link) {
            $http.put(baseUrl + "api/rating/" + link.id + "/?format=json&q=", {liked: !link.liked}).success(function (data, status) {
                link.liked = data.liked;
                link.likes = data.likes;
            });
        };

        $scope.changeOrderOption = function (option) {
            $scope.orderOption = option;
            $scope.nextPage = "";
            $scope.links = [];
            $scope.pollAllLinks();
        };

        $scope.pollAllLinks();
    }]);