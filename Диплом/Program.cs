using AirportSystem;
using Microsoft.EntityFrameworkCore;

internal class Program
{
    private static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);
        string connection = builder.Configuration.GetConnectionString("DefaultConnection");
        builder.Services.AddDbContext<ApplicationContext>(options => options.UseNpgsql(connection));

        // Добавление CORS
        builder.Services.AddCors(options =>
        {
            options.AddDefaultPolicy(
                builder =>
                {
                    builder.AllowAnyOrigin()
                           .AllowAnyMethod()
                           .AllowAnyHeader();
                });
        });

        var app = builder.Build();

        // Использование статических файлов и CORS
        app.UseDefaultFiles();
        app.UseStaticFiles();
        app.UseCors();

        // Department API
        app.MapGet("/api/department", async (ApplicationContext db) =>
        {
            return Results.Ok(await db.department.ToListAsync());
        });


        app.MapGet("/api/department/{id:int}", async (int id, ApplicationContext db) =>
        {
            var department = await db.department.FirstOrDefaultAsync(d => d.id == id);
            if (department == null) return Results.NotFound(new { message = "Отдел не найден" });
            return Results.Ok(department);
        });

        app.MapPost("/api/department", async (Department departmentData, ApplicationContext db) =>
        {
            await db.department.AddAsync(departmentData);
            await db.SaveChangesAsync();
            return Results.Ok(departmentData);
        });

        app.MapPut("/api/department/{id:int}", async (Department departmentData, ApplicationContext db) =>
        {
            var department = await db.department.FirstOrDefaultAsync(d => d.id == departmentData.id);
            if (department == null) return Results.NotFound(new { message = "Отдел не найден" });

            department.name = departmentData.name;
            department.phone = departmentData.phone;
            department.organization = departmentData.organization;

            await db.SaveChangesAsync();
            return Results.Ok(department);
        });

        app.MapDelete("/api/department/{id:int}", async (int id, ApplicationContext db) =>
        {
            var department = await db.department.FirstOrDefaultAsync(d => d.id == id);
            if (department == null) return Results.NotFound(new { message = "Отдел не найден" });

            db.department.Remove(department);
            await db.SaveChangesAsync();
            return Results.NoContent();
        });



        // Flight API
        app.MapGet("/api/flight", async (ApplicationContext db) =>
        {
            return Results.Ok(await db.flight.ToListAsync());
        });

        app.MapGet("/api/flight/{id:int}", async (int id, ApplicationContext db) =>
        {
            var flight = await db.flight.FirstOrDefaultAsync(f => f.id == id);
            if (flight == null) return Results.NotFound(new { message = "Рейс не найден" });
            return Results.Ok(flight);
        });

        app.MapPost("/api/flight", async (Flight flightData, ApplicationContext db) =>
        {
            await db.flight.AddAsync(flightData);
            await db.SaveChangesAsync();
            return Results.Ok(flightData); 
        });


        app.MapPut("/api/flight/{id:int}", async (Flight flightData, ApplicationContext db) =>
        {
            var flight = await db.flight.FirstOrDefaultAsync(f => f.id == flightData.id);
            if (flight == null) return Results.NotFound(new { message = "Рейс не найден" });

            flight.aircrafttype = flightData.aircrafttype;
            flight.route = flightData.route;

            await db.SaveChangesAsync();
            return Results.Ok(flight);
        });

        app.MapDelete("/api/flight/{id:int}", async (int id, ApplicationContext db) =>
        {
            var flight = await db.flight.FirstOrDefaultAsync(f => f.id == id);
            if (flight == null) return Results.NotFound(new { message = "Рейс не найден" });

            db.flight.Remove(flight);
            await db.SaveChangesAsync();
            return Results.NoContent();
        });

        // Passenger API
        app.MapGet("/api/passenger", async (ApplicationContext db) =>
        {
            return await db.passenger
                .Include(p => p.department)
                .Include(p => p.flight)
                .ToListAsync();
        });

        app.MapGet("/api/passenger/{id:int}", async (int id, ApplicationContext db) =>
        {
            var passenger = await db.passenger
                .Include(p => p.department)
                .Include(p => p.flight)
                .FirstOrDefaultAsync(p => p.id == id);

            return passenger == null
                ? Results.NotFound(new { message = "Пассажир не найден" })
                : Results.Ok(passenger);
        });

        app.MapPost("/api/passenger", async (Passenger passengerData, ApplicationContext db) =>
        {
            if (passengerData == null)
                return Results.BadRequest("Данные пассажира не предоставлены");

            // Проверка существования отдела и рейса
            var departmentExists = await db.department.AnyAsync(d => d.id == passengerData.departmentid);
            var flightExists = await db.flight.AnyAsync(f => f.id == passengerData.flightid);

            if (!departmentExists || !flightExists)
                return Results.BadRequest("Указанный отдел или рейс не существует");

            await db.passenger.AddAsync(passengerData);
            await db.SaveChangesAsync();
            return Results.Ok(passengerData);
        });

        app.MapPut("/api/passenger/{id:int}", async (Passenger passengerData, ApplicationContext db) =>
        {
            var passenger = await db.passenger.FirstOrDefaultAsync(p => p.id == passengerData.id);
            if (passenger == null) return Results.NotFound(new { message = "Пассажир не найден" });

            // Проверка существования отдела и рейса
            var departmentExists = await db.department.AnyAsync(d => d.id == passengerData.departmentid);
            var flightExists = await db.flight.AnyAsync(f => f.id == passengerData.flightid);

            if (!departmentExists || !flightExists)
            {
                return Results.BadRequest(new { message = "Указанный отдел или рейс не существует" });
            }

            passenger.fullname = passengerData.fullname;
            passenger.passport = passengerData.passport;
            passenger.birthday = passengerData.birthday;
            passenger.gender = passengerData.gender;
            passenger.position = passengerData.position;
            passenger.trippurpose = passengerData.trippurpose;
            passenger.departmentid = passengerData.departmentid;
            passenger.flightid = passengerData.flightid;
            passenger.plannedtransportdate = passengerData.plannedtransportdate;
            passenger.cargoweight = passengerData.cargoweight;
            passenger.notes = passengerData.notes;
            passenger.dp = passengerData.dp;
            passenger.zayavkadate = passengerData.zayavkadate;
            passenger.factdate = passengerData.factdate;
            passenger.zayavkanumber = passengerData.zayavkanumber;

            await db.SaveChangesAsync();
            return Results.Ok(passenger);
        });

        app.MapDelete("/api/passenger/{id:int}", async (int id, ApplicationContext db) =>
        {
            var passenger = await db.passenger.FirstOrDefaultAsync(p => p.id == id);
            if (passenger == null) return Results.NotFound(new { message = "Пассажир не найден" });

            db.passenger.Remove(passenger);
            await db.SaveChangesAsync();
            return Results.NoContent();
        });

        app.Run();
    }
}