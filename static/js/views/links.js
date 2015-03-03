var app = angular.module('LinksList', [])

app.controller("LinksListController", ['$scope', '$http',
    function ($scope, $http) {
        $scope.links = [];
        $scope.pollAllLinks = function () {
            $http
                .get(baseUrl + "api/allbookmarks/?format=json")
                .success(function (data, status) {
                    $scope.links = data.results;
                });
        }

        $scope.pollAllLinks();
    }])