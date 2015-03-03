var app = angular.module('LinksList', ['infinite-scroll'])

app.controller("LinksListController", ['$scope', '$http',
    function ($scope, $http) {
        $scope.links = [];
        $scope.nextPage = "";
        $scope.busy = false;
        $scope.pollAllLinks = function () {
            $scope.busy = true;
            var requestUrl = $scope.nextPage == "" ? baseUrl + "api/allbookmarks/?format=json" : $scope.nextPage;
            if($scope.nextPage != null){
                $http
                .get(requestUrl)
                .success(function (data, status) {
                    $scope.nextPage = data.next;
                    var items = data.results;
                    for(var i = 0; i < items.length; i++){
                        $scope.links.push(items[i]);
                    }

                    $scope.busy = false;
                });
            }
            else{
                $scope.busy = false;
            }

        }

        $scope.pollAllLinks();
    }])