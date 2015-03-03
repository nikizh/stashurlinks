var app = angular.module('LinksList', ['infinite-scroll', 'ngTagsInput'])

app.controller("LinksListController", ['$scope', '$http',
    function ($scope, $http) {
        $scope.links = [];
        $scope.nextPage = "";
        $scope.busy = false;
        $scope.searchOption = "Search Tags";
        $scope.searchMode = false;
        $scope.tags = [];
        $scope.pollAllLinks = function () {
            $scope.busy = true;
            if ($scope.searchMode) {
                tagIds = jQuery.map($scope.tags, function (t, i) {
                    return ( t.id );
                });
                var requestUrl = $scope.nextPage == "" ? baseUrl + "api/allbookmarks/?format=json&tagid=" + tagIds.toString() : $scope.nextPage;
            }
            else
                var requestUrl = $scope.nextPage == "" ? baseUrl + "api/allbookmarks/?format=json" : $scope.nextPage;

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
            if ($scope.tags.length > 0) {
                if ($scope.searchOption === "Search Tags") {
                    $scope.links = [];
                    $scope.searchMode = true;
                    $scope.pollAllLinks();
                }
            }
            else {
                $scope.searchMode = false;
                $scope.pollAllLinks();
            }

        }
        $scope.loadTags = function (query) {
            return $http.get(baseUrl + "api/alltags/?format=json&q=" + query);
        }

        $scope.pollAllLinks();
    }])