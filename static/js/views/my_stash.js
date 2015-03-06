var app = angular.module('MyStash', ['infinite-scroll', 'ngTagsInput'])

app.controller("MyStashController", ['$scope', '$http',
    function ($scope, $http) {
        $scope.links = [];
        $scope.nextPage = "";
        $scope.busy = false;
        $scope.searchOption = "Search Tags";
        $scope.visibilityOptions = [{name: "All", query: "all"}, {name: "Public", query: "pub"}, {
            name: "Private",
            query: "prv"
        }]
        $scope.visibilityOption = $scope.visibilityOptions[0];
        $scope.searchMode = false;
        $scope.tags = [];
        $scope.searchQuery = {q: ""};
        $scope.pollAllLinks = function () {
            $scope.busy = true;
            var queryUrl = "api/mybookmarks/?format=json"
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
            if($scope.visibilityOption !== $scope.visibilityOptions[0]){
                queryUrl = queryUrl + "&visibility=" + $scope.visibilityOption.query;
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

        }
        $scope.addTag = function (tag) {
            $scope.push(tag);
        }
        $scope.changeSearchOption = function (option) {
            $scope.searchOption = option;
        }
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

        }
        $scope.loadTags = function (query) {
            return $http.get(baseUrl + "api/alltags/?format=json&q=" + query);
        }
        $scope.changeVisibilityOption = function(option){
            $scope.nextPage = "";
            $scope.links = [];
            $scope.visibilityOption = option;
            $scope.pollAllLinks();
        }

        $scope.pollAllLinks();
    }])