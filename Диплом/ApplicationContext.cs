using Microsoft.EntityFrameworkCore;
using AirportSystem;

public class ApplicationContext : DbContext
{
    public DbSet<Department> department { get; set; }
    public DbSet<Flight> flight { get; set; }
    public DbSet<Passenger> passenger { get; set; }

    public ApplicationContext(DbContextOptions<ApplicationContext> options)
        : base(options)
    {
    }
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        //Первичные ключи
        modelBuilder.Entity<Department>().HasKey(d => d.id);
        modelBuilder.Entity<Flight>().HasKey(f => f.id);
        modelBuilder.Entity<Passenger>().HasKey(p => p.id);

        //Внешние ключи
        modelBuilder.Entity<Passenger>()
            .HasOne(p => p.department)
            .WithMany()
            .HasForeignKey(p => p.departmentid);

        modelBuilder.Entity<Passenger>()
            .HasOne(p => p.flight)
            .WithMany()
            .HasForeignKey(p => p.flightid);

        modelBuilder.Entity<User>(entity =>
        {
            entity.HasIndex(e => e.Username).IsUnique();
            entity.HasIndex(e => e.Email).IsUnique();
            entity.Property(e => e.CreatedAt).HasDefaultValueSql("CURRENT_TIMESTAMP");
        });



        modelBuilder.Entity<Department>().HasData(
            new Department { id = 4, name = "Белоярское УАВР",phone = null, organization = null },
            new Department { id = 5, name = "ИТЦ", phone = null, organization = null },
            new Department { id = 1, name = "Сосьвинское ЛПУМГ", phone = null, organization = null },
            new Department { id = 2, name = "Пунгинское ЛПУМГ", phone = null, organization = null },
            new Department { id = 3, name = "Югорское УАВР", phone = null, organization = null }
        );

        modelBuilder.Entity<Flight>().HasData(
            new Flight { id = 3, route = "Хулимсунт-Ивдель 1", aircrafttype = "МИ8АМТ"},
            new Flight { id = 4, route = "Советский-Белоярский",aircrafttype = "Л410" }
        );

        _ = modelBuilder.Entity<Passenger>().HasData(
            new Passenger
            {
                id = 4,fullname = null,passport = null,birthday = null,gender = "Муж",position = "Сотрудник ГТЮ",trippurpose = "Служебная поездка",
                departmentid = 1,plannedtransportdate = new DateOnly(2025, 1, 3),flightid = 1,cargoweight = null,notes=null,dp="C",zayavkadate = new DateOnly(2025, 01,02),
                factdate = new DateOnly(2025, 01, 02),zayavkanumber = 3
            });
    }
}