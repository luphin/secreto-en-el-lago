using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Text.Json;
using System.Text;
using System.Threading.Tasks;
using System.Collections.Generic;
using frontend.Models;

namespace frontend.Controllers
{
    public class LoanController : Controller
    {
        private readonly HttpClient _httpClient;
        private readonly string _apiBaseUrl;

        public LoanController(IHttpClientFactory httpClientFactory, IConfiguration configuration)
        {
            _httpClient = httpClientFactory.CreateClient();
            _apiBaseUrl = configuration["ApiSettings:BaseUrl"];
        }

        [HttpGet]
        public async Task<IActionResult> Index(string estado)
        {
            var accessToken = HttpContext.Session.GetString("AccessToken");
            if (string.IsNullOrEmpty(accessToken))
                return RedirectToAction("Login", "Auth");

            _httpClient.DefaultRequestHeaders.Authorization =
                new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", accessToken);

            var queryString = string.IsNullOrEmpty(estado) ? "" : $"?estado={estado}";
            var response = await _httpClient.GetAsync($"{_apiBaseUrl}/loans{queryString}");

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                var loans = JsonSerializer.Deserialize<List<LoanDto>>(content);
                ViewData["Estado"] = estado;
                return View(loans);
            }

            return View(new List<LoanDto>());
        }

        [HttpGet]
        public IActionResult Create()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Create(LoanDto model)
        {
            var accessToken = HttpContext.Session.GetString("AccessToken");
            if (string.IsNullOrEmpty(accessToken))
                return RedirectToAction("Login", "Auth");

            if (!ModelState.IsValid)
                return View(model);

            _httpClient.DefaultRequestHeaders.Authorization =
                new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", accessToken);

            var json = JsonSerializer.Serialize(model);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync($"{_apiBaseUrl}/loans", content);

            if (response.IsSuccessStatusCode)
            {
                return RedirectToAction("Index");
            }

            ModelState.AddModelError("", "Error al crear el préstamo");
            return View(model);
        }

        [HttpPost]
        public async Task<IActionResult> Return(string id)
        {
            var accessToken = HttpContext.Session.GetString("AccessToken");
            if (string.IsNullOrEmpty(accessToken))
                return RedirectToAction("Login", "Auth");

            _httpClient.DefaultRequestHeaders.Authorization =
                new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", accessToken);

            var response = await _httpClient.PostAsync($"{_apiBaseUrl}/loans/{id}/return", null);

            return RedirectToAction("Index");
        }

        [HttpGet]
        public async Task<IActionResult> Overdue()
        {
            var accessToken = HttpContext.Session.GetString("AccessToken");
            if (string.IsNullOrEmpty(accessToken))
                return RedirectToAction("Login", "Auth");

            _httpClient.DefaultRequestHeaders.Authorization =
                new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", accessToken);

            var response = await _httpClient.GetAsync($"{_apiBaseUrl}/loans/overdue");

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                var loans = JsonSerializer.Deserialize<List<LoanDto>>(content);
                return View(loans);
            }

            return View(new List<LoanDto>());
        }
    }
}
