# Synthetic Traffic Generator, Version 0.1
# (c) 2015-2015, Inria, Palaiseau, France
# Licensed under the GNU GPL, Version 3. For more details see LICENSE
# Author: Eduardo Mucelli Rezende Oliveira (edumucelli@gmail.com)

from datetime import datetime, date, timedelta
from multiprocessing import Process
from os import path, makedirs
from typing import Dict, Union, Tuple, Iterator

from numpy.random import seed, uniform
from scipy.stats import gamma, weibull_min, lognorm, nbinom

from log import debug

# Directory that will contain the resulting synthetic traffic.
# Automatically created if does not exist.
USERS_DIRECTORY = "users"
# Directory that contains the synthetic request files, one per synthetic user
SYNTHETIC_DIRECTORY = "synthetic"

ONE_HOUR = 3600
ONE_DAY = ONE_HOUR * 24

# The number of resulting synthetic users
NUMBER_OF_SYNTHETIC_USERS = 10


class Distribution(object):
    def __init__(self, user_class, hour):
        self.user_class = user_class
        self.hour = hour
        self.name = None


class VolumeDistribution(Distribution):
    def __init__(self, user_class, hour):
        Distribution.__init__(self, user_class, hour)

    def choose(self) -> weibull_min:
        self.name = "Weibull"
        if self.user_class == "HF":
            peak_hours_for_volume_hf = [10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
            if self.hour in peak_hours_for_volume_hf:
                weibull_c_shape, weibull_scale, weibull_location = 0.819409132355671, 774639.610211396, 40
                return weibull_min(weibull_c_shape, loc=weibull_location, scale=weibull_scale)
            else:
                weibull_c_shape, weibull_scale, weibull_location = 0.634477150024807, 384935.669023795, 40
                return weibull_min(weibull_c_shape, loc=weibull_location, scale=weibull_scale)
        elif self.user_class == "HO":
            peak_hours_for_volume_ho = [1, 2, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 19, 21]
            if self.hour in peak_hours_for_volume_ho:
                weibull_c_shape, weibull_scale, weibull_location = 0.498273622342091, 476551.703412746, 30
            else:
                weibull_c_shape, weibull_scale, weibull_location = 0.507073160695169, 452332.836400453, 30
            return weibull_min(weibull_c_shape, loc=weibull_location, scale=weibull_scale)
        elif self.user_class == "MF":
            peak_hours_for_volume_mf = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
            if self.hour in peak_hours_for_volume_mf:
                weibull_c_shape, weibull_scale, weibull_location = 0.801202265360056, 13959.452422549, 37
                return weibull_min(weibull_c_shape, loc=weibull_location, scale=weibull_scale)
            else:
                weibull_c_shape, weibull_scale, weibull_location = 0.797283673532605, 10657.9935943482, 33
                return weibull_min(weibull_c_shape, loc=weibull_location, scale=weibull_scale)
        elif self.user_class == "MO":
            peak_hours_for_volume_mo = [1, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
            if self.hour in peak_hours_for_volume_mo:
                weibull_c_shape, weibull_scale, weibull_location = 0.596142171663733, 31936.8353050143, 29
            else:
                weibull_c_shape, weibull_scale, weibull_location = 0.588535361156048, 26617.7612810844, 30
            return weibull_min(weibull_c_shape, loc=weibull_location, scale=weibull_scale)
        elif self.user_class == "LF":
            peak_hours_for_volume_lf = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
            if self.hour in peak_hours_for_volume_lf:
                weibull_c_shape, weibull_scale, weibull_location = 0.926450022452343, 1181.70293939011, 33
            else:
                weibull_c_shape, weibull_scale, weibull_location = 1.03429757728009, 873.579218199549, 34
            return weibull_min(weibull_c_shape, loc=weibull_location, scale=weibull_scale)
        elif self.user_class == "LO":
            peak_hours_for_volume_lo = [1, 3, 4, 19, 20, 21, 22, 23]
            if self.hour in peak_hours_for_volume_lo:
                weibull_c_shape, weibull_scale, weibull_location = 0.856409898006734, 3228.75558535546, 29
            else:
                weibull_c_shape, weibull_scale, weibull_location = 0.797856625454382, 2800.11615587819, 29
            return weibull_min(weibull_c_shape, loc=weibull_location, scale=weibull_scale)
        else:
            raise Exception("The user class %s does not exist" % self.user_class)


class IATDistribution(Distribution):
    def __init__(self, user_class, hour):
        Distribution.__init__(self, user_class, hour)

    def choose(self) -> Union[lognorm, gamma, weibull_min]:
        if self.user_class == "HF":
            self.name = "Log-norm"
            peak_hours_for_iat_hf = [1, 2, 3, 4, 5, 6]
            if self.hour in peak_hours_for_iat_hf:
                lognorm_shape, lognorm_scale, lognorm_location = 4.09174469261446, 1.12850165892419, 4.6875
            else:
                lognorm_shape, lognorm_scale, lognorm_location = 3.93740014906562, 0.982210300411203, 3
            return lognorm(lognorm_shape, loc=lognorm_location, scale=lognorm_scale)
        elif self.user_class == "HO":
            self.name = "Gamma"
            peak_hours_for_iat_ho = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
            if self.hour in peak_hours_for_iat_ho:
                gamma_shape, gamma_rate, gamma_location = 1.25170029089175, 0.00178381168026473, 0.5
            else:
                gamma_shape, gamma_rate, gamma_location = 1.20448161464647, 0.00177591076721503, 0.5
            return gamma(gamma_shape, loc=gamma_location, scale=1.0 / gamma_rate)
        elif self.user_class == "MF":
            self.name = "Gamma"
            peak_hours_for_iat_mf = [1, 2, 3, 4, 5, 6, 7, 22, 23]
            if self.hour in peak_hours_for_iat_mf:
                gamma_shape, gamma_rate, gamma_location = 2.20816848575484, 0.00343216949000565, 1
            else:
                gamma_shape, gamma_rate, gamma_location = 2.03011412986896, 0.00342699308280547, 1
            return gamma(gamma_shape, loc=gamma_location, scale=1.0 / gamma_rate)
        elif self.user_class == "MO":
            self.name = "Gamma"
            peak_hours_for_iat_mo = [1, 2, 3, 4, 5, 6]
            if self.hour in peak_hours_for_iat_mo:
                gamma_shape, gamma_rate, gamma_location = 1.29908195595742, 0.00163527376977441, 0.5
            else:
                gamma_shape, gamma_rate, gamma_location = 1.19210494792398, 0.00170354443324898, 0.5
            return gamma(gamma_shape, loc=gamma_location, scale=1.0 / gamma_rate)
        elif self.user_class == "LF":
            peak_hours_for_iat_lf = [1, 2, 3, 4, 5, 6, 7]
            if self.hour in peak_hours_for_iat_lf:
                self.name = "Gamma"
                gamma_shape, gamma_rate, gamma_location = 1.79297773527656, 0.00191590321039876, 2
                return gamma(gamma_shape, loc=gamma_location, scale=1.0 / gamma_rate)
            else:
                self.name = "Weibull"
                weibull_c_shape, weibull_scale, weibull_location = 1.1988117443903, 827.961760834184, 1
                return weibull_min(weibull_c_shape, loc=weibull_location, scale=weibull_scale)
        elif self.user_class == "LO":
            peak_hours_for_iat_lo = [2, 3, 4, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20]
            if self.hour in peak_hours_for_iat_lo:
                self.name = "Weibull"
                weibull_c_shape, weibull_scale, weibull_location = 0.850890858519732, 548.241539446292, 1
                return weibull_min(weibull_c_shape, loc=weibull_location, scale=weibull_scale)
            else:
                self.name = "Gamma"
                gamma_shape, gamma_rate, gamma_location = 0.707816241615835, 0.00135537879658998, 1
                return gamma(gamma_shape, loc=gamma_location, scale=1.0 / gamma_rate)
        else:
            raise Exception("The user class %s does not exist" % self.user_class)


class NumberOfRequestsDistribution(Distribution):
    def __init__(self, user_class, hour):
        Distribution.__init__(self, user_class, hour)

    def choose(self) -> nbinom:
        self.name = "Neg-binomial"
        if self.user_class == "HF":
            peak_hours_for_number_of_requests_hf = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
            if self.hour in peak_hours_for_number_of_requests_hf:
                nbinom_n_size, nbinom_mu_mean = 0.470368548315641, 34.7861725808564
            else:
                nbinom_n_size, nbinom_mu_mean = 0.143761308534382, 14.158264589062
        elif self.user_class == "HO":
            peak_hours_for_number_of_requests_ho = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
            if self.hour in peak_hours_for_number_of_requests_ho:
                nbinom_n_size, nbinom_mu_mean = 0.113993444740046, 1.04026982546095
            else:
                nbinom_n_size, nbinom_mu_mean = 0.0448640346452827, 0.366034837767499
        elif self.user_class == "MF":
            peak_hours_for_number_of_requests_mf = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
            if self.hour in peak_hours_for_number_of_requests_mf:
                nbinom_n_size, nbinom_mu_mean = 0.758889839349924, 4.83390315655562
            else:
                nbinom_n_size, nbinom_mu_mean = 0.314653746175354, 3.22861572712093
        elif self.user_class == "MO":
            peak_hours_for_number_of_requests_mo = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
            if self.hour in peak_hours_for_number_of_requests_mo:
                nbinom_n_size, nbinom_mu_mean = 0.177211316065872, 0.406726610288464
            else:
                nbinom_n_size, nbinom_mu_mean = 0.0536955764781434, 0.124289074773539
        elif self.user_class == "LF":
            peak_hours_for_number_of_requests_lf = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
            if self.hour in peak_hours_for_number_of_requests_lf:
                nbinom_n_size, nbinom_mu_mean = 0.480203280455517, 0.978733578849008
            else:
                nbinom_n_size, nbinom_mu_mean = 0.240591506072217, 0.487956906502501
        elif self.user_class == "LO":
            peak_hours_for_number_of_requests_lo = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
            if self.hour in peak_hours_for_number_of_requests_lo:
                nbinom_n_size, nbinom_mu_mean = 0.188551092877969, 0.111187768162793
            else:
                nbinom_n_size, nbinom_mu_mean = 0.0810585648991726, 0.0405013083716073
        else:
            raise Exception("The user class %s does not exist" % self.user_class)
        # From R's documentation: An alternative parametrization (often used in ecology) is by the
        #  _mean_ 'mu', and 'size', the _dispersion parameter_, where 'prob' = 'size/(size+mu)'
        nbinom_prob = nbinom_n_size / (nbinom_n_size + nbinom_mu_mean)
        return nbinom(nbinom_n_size, nbinom_prob)


class TrafficModel(object):
    def __init__(self, user_class="HF", hour=1):
        # Gamma or Weibull distributed in KiloBytes
        self.volume_distribution = VolumeDistribution(user_class, hour).choose()
        # Gamma or Log-normal distributed in seconds
        self.iat_distribution = IATDistribution(user_class, hour).choose()
        # Negative binomial
        self.number_of_requests_distribution = NumberOfRequestsDistribution(user_class, hour).choose()


class User(object):
    def __init__(self, uid, klass, initial_timestamp_date=datetime.utcnow()):
        self.uid = uid
        self.klass = klass

        self.initial_timestamp_date = initial_timestamp_date
        # Remember, hours from 1 to 23, 0 was removed because it is behaving awkwardly
        self.hours = range(1, 24)

        # {1: TrafficModel, 2: TrafficModel, ...}
        self.traffic_model_per_hour = self.find_traffic_model_per_hour()

        self.request_arrival_times_per_hour = dict((hour, []) for hour in self.hours)
        self.request_arrival_datetimes_per_hour = dict((hour, []) for hour in self.hours)
        self.request_file_sizes_per_hour = dict((hour, []) for hour in self.hours)

    # Set the traffic model that corresponds to the user class, e.g,
    # 'HF' + peak hour => Volume {Weibull or Gamma}, Number of requests {Neg-Binomial}, ...
    def find_traffic_model_per_hour(self) -> Dict[int, TrafficModel]:
        traffic_model_per_hour = {}
        for hour in self.hours:
            traffic_model_per_hour[hour] = TrafficModel(self.klass, hour)
        return traffic_model_per_hour

    #  def generate_synthetic_traffic(self):
    #    first_hour = self.hours[0]
    #    next_arrival_time_in_seconds = 0
    #    next_arrival_datetime = datetime(self.initial_timestamp_date.year, self.initial_timestamp_date.month, self.initial_timestamp_date.day, first_hour)
    #    while True:
    #      next_arrival_time_in_seconds += self.traffic_model_per_hour[next_arrival_datetime.hour].iat_distribution.rvs()
    #      next_arrival_datetime = datetime(self.initial_timestamp_date.year, self.initial_timestamp_date.month, self.initial_timestamp_date.day, first_hour) + timedelta(seconds=next_arrival_time_in_seconds)
    #      if next_arrival_datetime.day == self.initial_timestamp_date.day:
    #        self.session_arrival_datetimes_per_hour[next_arrival_datetime.hour].append(next_arrival_datetime)
    #      else:
    #        break
    #    for hour, session_arrival_datetimes in self.session_arrival_datetimes_per_hour.iteritems():
    #      number_of_requests_within_hour = len(session_arrival_datetimes)
    #      # volume represents the total volume in the hour 'hour'
    #      volume_within_hour = self.traffic_model_per_hour[hour].volume_distribution.rvs()
    ##      if number_of_requests_within_hour > 0:
    ##        self.session_volumes_per_hour[hour] = number_of_requests_within_hour * [volume_within_hour / number_of_requests_within_hour]
    ##      else:
    ##        self.session_volumes_per_hour[hour] = number_of_requests_within_hour * [0]
    #      # the total volume in this hour will be equally divided by the number of requests
    #      for session_arrival_datetime in session_arrival_datetimes:
    #        volume_within_hour_per_session = volume_within_hour / number_of_requests_within_hour
    #        self.session_volumes_per_hour[session_arrival_datetime.hour].append(volume_within_hour_per_session)

    #  def requests(self):
    #    for hour self.hours:
    #      for session_volume, session_arrival_datetime in zip(self.session_volumes_per_hour[hour], self.session_arrival_datetimes_per_hour[hour]):
    #        yield [session_volume, session_arrival_datetime]

    def generate_synthetic_traffic(self) -> None:
        for hour, traffic_model in self.traffic_model_per_hour.items():
            number_of_requests = traffic_model.number_of_requests_distribution.rvs()

            if number_of_requests > 0:
                mean_inter_arrival_times = []
                if number_of_requests == 1:
                    mean_inter_arrival_times.append(traffic_model.iat_distribution.rvs())
                else:
                    # The number of requests and inter arrival times are generated by two different distributions and
                    # here is the drawback: If the number of requests is big, the IAT should be distributed in small
                    # values in order to not surpass one hour, But the IATDistribution is not aware about how many
                    # requests were generated, they are two independent variables. Therefore, we have to resample the
                    # mean IATs, that summed up, would not go beyond one hour.
                    mean_inter_arrival_times_attempt = traffic_model.iat_distribution.rvs(size=number_of_requests)
                    attempt = 0
                    while sum(mean_inter_arrival_times_attempt) > ONE_HOUR and attempt <= 100000:
                        mean_inter_arrival_times_attempt = traffic_model.iat_distribution.rvs(size=number_of_requests)
                        attempt += 1
                    mean_inter_arrival_times.extend(mean_inter_arrival_times_attempt)

                # The number of requests and inter arrival times are generated by two different distributions and
                # here is the drawback: If the number of requests is big, the IAT should be distributed in small
                # values in order to not surpass one hour, But the IATDistribution is not aware about how many
                # requests were generated, they are two independent variables. Therefore, we have to remove requests,
                # mean IAT and arrival times, that summed up, would go beyond one hour.
                while sum(mean_inter_arrival_times) > ONE_HOUR:
                    number_of_requests -= 1
                    mean_inter_arrival_times.pop()

                arrival_times = []
                arrival_datetimes = []
                for index, time in enumerate(mean_inter_arrival_times):
                    if index == 0:
                        arrival_times.append(time)
                        arrival_datetimes.append(
                            datetime(
                                self.initial_timestamp_date.year,
                                self.initial_timestamp_date.month,
                                self.initial_timestamp_date.day,
                                hour,
                            )
                            + timedelta(seconds=time)
                        )
                    else:
                        arrival_times.append(arrival_times[index - 1] + time)
                        arrival_datetimes.append(
                            datetime(
                                self.initial_timestamp_date.year,
                                self.initial_timestamp_date.month,
                                self.initial_timestamp_date.day,
                                hour,
                            )
                            + timedelta(seconds=arrival_times[index - 1] + time)
                        )
                self.request_arrival_times_per_hour[hour].extend(arrival_times)
                self.request_arrival_datetimes_per_hour[hour].extend(arrival_datetimes)

                volumes_of_traffic = []
                # The distribution for the volume of traffic was measure for the *whole* hour. It means that each
                # sampling from the volume_distribution returns the expected volume for the whole hour. We have then
                # to divide this volume by the number of requests in that hour to have one volume per request.
                # traffic_model.volume_distribution.rvs(size = number_of_requests) / number_of_requests - this snipt
                # generates an array with one volume of traffic per request and divide *all at the same time* by the
                # number of requests
                volumes_of_traffic.extend(
                    traffic_model.volume_distribution.rvs(size=number_of_requests) / number_of_requests
                )
                self.request_file_sizes_per_hour[hour].extend(volumes_of_traffic)

    def requests(self) -> Iterator[Tuple[float, datetime]]:
        for hour in range(1, 24):
            for filesize, arrival_datetime in zip(
                self.request_file_sizes_per_hour[hour], self.request_arrival_datetimes_per_hour[hour]
            ):
                yield [filesize, arrival_datetime]

    def write_traffic_to_file(self) -> None:
        user_syntethic_trace_path = path.join(USERS_DIRECTORY, SYNTHETIC_DIRECTORY)
        if not path.exists(user_syntethic_trace_path):
            makedirs(user_syntethic_trace_path)
        debug("Generating synthetic traffic for user %s" % self.uid)
        with open(path.join(user_syntethic_trace_path, "%s.dat" % self.uid), "w") as user_syntethic_trace_file:
            for filesize, arrival_datetime in self.requests():
                # Remove the microsecond part from the datetime
                user_syntethic_trace_file.write(
                    "%s %s %s %s\n" % (arrival_datetime.strftime("%Y-%m-%d %H:%M:%S"), self.uid, filesize, self.klass)
                )  # 2013-08-25 00:10:58 13 30.7411159743, HF

    def generate_and_write_synthetic_traffic(self) -> None:
        # Numpy has the same seed for each child process, thus users sharing
        # the same distributions get same values from rvs method
        # A way workaround this is to reseed for every process spawned by multiprocessing
        # http://stackoverflow.com/a/14505947/914874
        #    pid = current_process()._identity[0]
        #    seed(pid)
        seed(self.uid)
        self.generate_synthetic_traffic()
        self.write_traffic_to_file()


class UserDistribution(object):
    def __init__(self, number_of_users):
        self.number_of_users = number_of_users
        self.total_number_of_users = number_of_users

        # Empirical probabilities from the original's dataset distribution given by
        # the number of users on a category divided by the total number of users
        self.mo_probability = 0.39444894558049604  # 598340
        self.lo_probability = 0.26755074985117683  # 405848
        self.ho_probability = 0.31970379082089073  # 484959
        self.lf_probability = 0.008566808249186994  # 12995
        self.mf_probability = 0.008291246429397832  # 12577
        self.hf_probability = 0.0014384590688515599  # 2182

    def users(self) -> Iterator[User]:
        for uid in range(self.number_of_users):
            # uniformly randomly choose an user class based on their probabilities
            probability = uniform()
            if probability <= self.mo_probability:
                klass = "MO"
            elif probability <= self.mo_probability + self.lo_probability:
                klass = "LO"
            elif probability <= self.mo_probability + self.lo_probability + self.ho_probability:
                klass = "HO"
            elif probability <= self.mo_probability + self.lo_probability + self.ho_probability + self.lf_probability:
                klass = "LF"
            elif (
                probability
                <= self.mo_probability
                + self.lo_probability
                + self.ho_probability
                + self.lf_probability
                + self.mf_probability
            ):
                klass = "MF"
            else:
                klass = "HF"
            yield User(uid, klass)


def generate_synthethic_users_and_traffic(number_of_users=NUMBER_OF_SYNTHETIC_USERS) -> None:
    # Makes the random numbers predictable, to make the experiment reproducible.
    seed(1234)
    user_generator = UserDistribution(number_of_users)
    # generate_and_write_synthetic_traffic is a very light method, thus it
    # is not necessary to create a pool of processes and join them later on
    for user in user_generator.users():
        Process(target=user.generate_and_write_synthetic_traffic).start()
