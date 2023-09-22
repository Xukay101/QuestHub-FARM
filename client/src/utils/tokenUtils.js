function isTokenExpired(token) {
    if (!token) return true;

    const tokenData = JSON.parse(atob(token.split('.')[1]));
    const tokenExpiration = tokenData.exp * 1000; 

    return tokenExpiration < Date.now();
}

export default isTokenExpired;