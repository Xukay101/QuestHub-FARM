export function isTokenExpired(token) {
    if (!token) return true;

    const tokenData = JSON.parse(atob(token.split('.')[1]));
    const tokenExpiration = tokenData.exp * 1000;

    return tokenExpiration < Date.now();
}

export function isAuthenticated() {
    const userDataString = localStorage.getItem('userData') || sessionStorage.getItem('userData');

    if (userDataString) {
        const userData = JSON.parse(userDataString);
        const accessToken = userData.access_token;

        if (accessToken && !isTokenExpired(accessToken)) {
            return true;
        }
    }

    return false;
}
