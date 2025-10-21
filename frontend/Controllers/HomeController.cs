using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using System.Collections.Generic;
using frontend.Models;

namespace frontend.Controllers
{
    public class HomeController : Controller
    {
        private readonly HttpClient _httpClient;
        private readonly string _apiBaseUrl;

        public HomeController(IHttpClientFactory httpClientFactory, IConfiguration configuration)
        {
            _httpClient = httpClientFactory.CreateClient();
            _apiBaseUrl = configuration["ApiSettings:BaseUrl"];
        }

        public async Task<IActionResult> Index(string titulo, string autor, string categoria, string search, string anonymous)
        {
            // Si el usuario no está autenticado y no solicitó continuar como anónimo,
            // redirigir a la página de login primero.
            if (HttpContext.Session.GetString("AccessToken") == null && anonymous != "true")
            {
                return RedirectToAction("Login", "Auth");
            }

            var documents = new List<DocumentDto>();

            // Build query parameters
            var queryParams = new List<string>();
            if (!string.IsNullOrEmpty(titulo)) queryParams.Add($"titulo={titulo}");
            if (!string.IsNullOrEmpty(autor)) queryParams.Add($"autor={autor}");
            if (!string.IsNullOrEmpty(categoria)) queryParams.Add($"categoria={categoria}");
            if (!string.IsNullOrEmpty(search)) queryParams.Add($"search={search}");

            var queryString = queryParams.Count > 0 ? "?" + string.Join("&", queryParams) : "";

            var response = await _httpClient.GetAsync($"{_apiBaseUrl}/documents{queryString}");

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                documents = JsonSerializer.Deserialize<List<DocumentDto>>(content);
            }

            ViewData["Titulo"] = titulo;
            ViewData["Autor"] = autor;
            ViewData["Categoria"] = categoria;
            ViewData["Search"] = search;
            ViewData["IsAnonymous"] = anonymous == "true";

            return View(documents);
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = System.Diagnostics.Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
