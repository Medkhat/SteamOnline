let testTabs = function() {
    let tabNav = document.querySelectorAll('.tab_nav_item'),
        tabContent = document.querySelectorAll('.tab_content_item'),
        tabName;

    tabNav.forEach(item => {
        item.addEventListener('click', selectTabNav);
    }); 

    function selectTabNav() {
        tabNav.forEach(item => {
            item.classList.remove('is-active');
        });
        this.classList.add('is-active');
        tabName = this.getAttribute('data-tabName');
        selectTabContent(tabName);
    }

    function selectTabContent(tabName) {
        tabContent.forEach(item => {
            item.classList.contains(tabName) ? item.classList.add('is-active') : item.classList.remove('is-active'); 
        });
    }
};

testTabs();