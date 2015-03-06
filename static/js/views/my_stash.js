var app = angular.module('MyStash', ['infinite-scroll', 'ngTagsInput', 'ui.bootstrap'])

app.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller("MyStashController", ['$scope', '$http', '$modal',
    function ($scope, $http, $modal) {
        $scope.links = [];
        $scope.nextPage = "";
        $scope.busy = false;
        $scope.searchOption = "Search Tags";
        $scope.visibilityOptions = [
            {name: "All", query: "all", icon: "glyphicon-th"},
            {name: "Public", query: "pub", icon: "glyphicon-eye-open"},
            {name: "Private", query: "prv", icon: "glyphicon-lock"}
        ];
        $scope.visibilityOption = $scope.visibilityOptions[0];
        $scope.searchMode = false;
        $scope.tags = [];
        $scope.searchQuery = {q: ""};
        $scope.pollAllLinks = function () {
            $scope.busy = true;
            var queryUrl = "api/mybookmarks/?format=json";
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
            if ($scope.visibilityOption !== $scope.visibilityOptions[0]) {
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
        $scope.changeVisibilityOption = function (option) {
            $scope.nextPage = "";
            $scope.links = [];
            $scope.visibilityOption = option;
            $scope.pollAllLinks();
        };

        $scope.open = function (item) {

            var modalInstance = $modal.open({
                templateUrl: 'my_stash_edit.html',
                controller: 'MyStashEditCtrl',
                resolve: {
                    item: function () {
                        return angular.copy(item);
                    }
                }
            });

            modalInstance.result.then(function (selectedItem) {
                angular.copy(selectedItem, item);
            }, function () {
            });
        };

        $scope.openDelete = function (item) {

            var modalInstance = $modal.open({
                templateUrl: 'my_stash_delete.html',
                controller: 'MyStashDeleteCtrl',
                resolve: {
                    item: function () {
                        return angular.copy(item);
                    }
                }
            });

            modalInstance.result.then(function () {
                var ind = $scope.links.indexOf(item);
                $scope.links.splice(ind, 1);
            }, function () {
            });
        };

        $scope.openAdd = function () {

            var modalInstance = $modal.open({
                templateUrl: 'my_stash_add.html',
                controller: 'MyStashAddCtrl'
            });

            modalInstance.result.then(function (newItem) {
                $scope.links.splice(0, 0, newItem);
            }, function () {

            });
        };

        $scope.pollAllLinks();
    }]);

app.controller('MyStashEditCtrl', function ($scope, $modalInstance, $http, item) {

    $scope.item = item;
    $scope.canSave = true;

    $scope.loadTags = function (query) {
        return $http.get(baseUrl + "api/alltags/?format=json&q=" + query);
    };

    $scope.save = function () {
        $scope.canSave = false; // disable the save button
        $http
            .put(baseUrl + "api/mybookmarks/" + $scope.item.id + "/", $scope.item)
            .success(function (data, status) {
                var item = data;
                $modalInstance.close(item);
            });
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});

app.controller('MyStashDeleteCtrl', function ($scope, $modalInstance, $http, item) {

    $scope.item = item;
    $scope.canDelete = true;

    $scope.delete = function () {
        $scope.canDelete = false; // disable the delete button
        $http
            .delete(baseUrl + "api/mybookmarks/" + $scope.item.id + "/")
            .success(function (data, status) {
                $modalInstance.close();
            });
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});

app.controller('MyStashAddCtrl', function ($scope, $modalInstance, $http) {

    $scope.canSave = true;

    $scope.item = {
        'public': false,
        'thumb': 'dummy_data', // placeholder data
        'date_created': "1970-01-01T00:00:00" // placeholder data
    };

    $scope.loadTags = function (query) {
        return $http.get(baseUrl + "api/alltags/?format=json&q=" + query);
    };

    $scope.save = function () {
        $scope.canSave = false; // disable the save button
        $http
            .post(baseUrl + "api/mybookmarks/?format=json", $scope.item)
            .success(function (data, status) {
                var item = data;
                $modalInstance.close(item);
            });
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});