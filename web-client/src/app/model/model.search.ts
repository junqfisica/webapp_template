export class Search {
    public searchParms = {
      "searchBy" : "",
      "searchValue" :  "",
      "orderBy" : "",
      "orderDesc" : null,
      "page" : null,
      "perPage" : null 
    };
  
    constructor(searchBy: string, value: string) {
      this.searchParms.searchBy = searchBy
      this.searchParms.searchValue = value
      this.searchParms.orderDesc = false 
      this.searchParms.page = 1
      this.searchParms.perPage = 10
    }
}